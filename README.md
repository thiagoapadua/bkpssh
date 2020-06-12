Script em python para backup de equipamentos Ubiquiti e Mikrotik por SSH

### Arquivo bkp-equip.py: Variáveis de configuração:
- _BKPDIR = "/home/bkpssh/arquivos" - Diretório onde os arquivos de backup serão salvos
- _HOSTFILE = "/root/bkpssh/equipamentos.txt" - Arquivo com informações dos equipamentos que serão feitos os backups
- _LOGFILE = "/root/scripts/bkp-equip.log" - Arquivo de Log do script
- _DIASBKP = "10" - Quantidade de dias de retenção dos backups
- _LOCKFILE = "/tmp/bkp-equip.lock" - Arquivo lock do script, impede de rodar duas instância

### Arquivo: equipamentos.txt: Lista dos equipamentos
- formato do arquivo;  
ros|ubnt:ip:port:user:pass:name  
Onde:  
  ros: Equipamentos RouterOS Mikrotik  
  ubnt: Equipamentos Ubiquiti  
Exemplo:  
  ros:172.16.1.51:22:admin:senha:Mikrotik-POP-1  
  ubnt:172.16.0.202:22:admin:senha:Rocket-Setorial-1  
  
### Agendamento
Adicionar ao cron a linha a seguir para executar o backup diariamente às 02:00 da manhã.
00 02 * * * /root/bkpssh/bkp-equip.py

