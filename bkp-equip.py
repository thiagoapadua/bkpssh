#!/usr/bin/env python

import paramiko, time, os, sys, logging, socket

logging.basicConfig()

_BKPDIR = "rede"
_HOSTFILE = "equipamentos.txt"
_LOGFILE = "bkp-equip.log"
_DIASBKP = "10"
_LOCKFILE = "/tmp/bkp-equip.lock"
_TIMEOUT = 10


if os.path.exists(_LOCKFILE):
        print ("Existe outra instancia do script bkp-equip.py em andamento")
        sys.exit(-1)
else:
        open(_LOCKFILE, 'w').write("1")
        try:
                arquivo = open(_HOSTFILE, 'r')
                arqlog = open(_LOGFILE,"w")

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
                                        ssh.connect(h_ip, port=h_porta, username=h_usuario, password=h_senha, timeout=_TIMEOUT, look_for_keys=False)
                                        ssh_stdin,ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
                                        data = ssh_stdout.read()
                                        ssh.close()
                                except socket.error as esock:
                                        arqlog.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Erro com host " + h_nome + "(" + h_ip  + ") " + str(esock) + "\n")
                                        continue
                                except paramiko.SSHException as essh:
                                        arqlog.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Erro com host " + h_nome + "(" + h_ip  + ") " + str(essh) + "\n")
                                        continue


                                dstfile = open(pathCompleto + "/" + nomearqdst, "wb")
                                dstfile.write(data)
                                dstfile.close()

        except Exception as ex:
                arqlog.write(time.strftime("%Y-%m-%d %H:%M:%S") + " Erro com host " + h_nome + "(" + h_ip  + ") " + str(ex) + "\n")

        finally:
                arquivo.close()
                arqlog.close()
                os.system("find " + _BKPDIR + " -mtime +" + _DIASBKP + " -exec rm -rf {} +")
                os.system("find " + _BKPDIR + " -type d -empty -exec rmdir {} +")
                os.remove(_LOCKFILE)
