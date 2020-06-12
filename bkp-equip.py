#!/usr/bin/env python

import paramiko, time, os, sys, logging, socket

logging.basicConfig()

_BKPDIR = "/home/bkpssh/rede"
_HOSTFILE = "/root/bkpssh/equipamentos.txt"
_LOGFILE = "/root/bkpssh/bkp-equip.log"
_DIASBKP = "10"
_LOCKFILE = "/tmp/bkp-equip.lock"

if os.path.exists(_LOCKFILE):
        print "Existe outra instancia do script bkp-equip.py em andamento"
        sys.exit(-1)
else:
        open(_LOCKFILE, 'w').write("1")
        try:
                arquivo = open(_HOSTFILE, 'r')
                arqlog = open(_LOGFILE,"w",0)

                for linha in arquivo:
                        if not linha.lstrip().startswith('#'):
                                host = linha.split(':')
                                h_tipo = host[0]
                                h_ip = host[1]
                                h_porta = int(host[2])
                                h_usuario = host[3]
                                h_senha = host[4]
                                h_nome = host[5].replace('\n','')

                                data = time.strftime("%Y-%m-%d")

                                pathCompleto = _BKPDIR + "/" + data

                                if not os.path.exists(pathCompleto):
                                        os.makedirs(pathCompleto)

                                if h_tipo == "ros":
                                        nomearqdst = h_nome + '.export'
                                        cmd = "export"
                                else:
                                        nomearqdst = h_nome + '.cfg'
                                        cmd = "cat /tmp/system.cfg"

                                arqlog.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Conectando em " + h_nome + "(" + h_ip  + ")\n")

                                try:
                                        ssh = paramiko.SSHClient()
                                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                                        ssh.connect(h_ip, h_porta, username=h_usuario, password=h_senha)
                                        ssh_stdin,ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
                                        data = ssh_stdout.read()
                                        ssh.close()
                                except socket.error, esock:
                                        arqlog.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Erro com host " + h_nome + "(" + h_ip  + ") " + str(esock) + "\n")
                                        continue
                                except paramiko.SSHException, essh:
                                        arqlog.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Erro com host " + h_nome + "(" + h_ip  + ") " + str(essh) + "\n")
                                        continue


                                dstfile = open(pathCompleto + "/" + nomearqdst, "w")
                                dstfile.write(data)
                                dstfile.close()

        except Exception, ex:
                arqlog.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Erro com host " + h_nome + "(" + h_ip  + ") " + str(ex) + "\n")

        finally:
                arquivo.close()
                arqlog.close()
                os.system("find " + _BKPDIR + " -mtime +" + _DIASBKP + " -exec rm -rf {} +")
                os.system("find " + _BKPDIR + " -type d -empty -exec rmdir {} +")
                os.remove(_LOCKFILE)
