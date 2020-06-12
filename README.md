# bkpssh
Script em python para backup de equipamentos Ubiquiti e Mikrotik por SSH

É necessário a configuração no arquivo bkpssh.py das variáveis a seguir:

# Diretório onde os arquivos de backup serão salvos
_BKPDIR = "/home/bkpssh/arquivos"
# Arquivo com informações dos equipamentos que serão feitos os backups
_HOSTFILE = "/root/bkpssh/equipamentos.txt"
# Arquivo de Log do script
_LOGFILE = "/root/scripts/bkp-equip.log"
# Quantidade de dias de retenção dos backups
_DIASBKP = "10"
#Arquivo lock do script, impede de rodar duas instâncias
_LOCKFILE = "/tmp/bkp-equip.lock"
