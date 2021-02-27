#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess,os,re,sys
import datetime
import time
from subprocess import check_output


def get_datetime():
    now = datetime.datetime.now()
    hora_data = now.strftime("%d/%m/%Y, %H:%M:%S")
    return hora_data

""" Set log file """
logfile = open('/tmp/install_netbox.log', 'a')

def set_log(status,msg):
    logfile.write('{} : {} : {}\n'.format(get_datetime(),status,msg))
    
""" get linux distro """
def get_distro():
    cmd = 'cat /etc/os-release'
    cmd_obj = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    output = cmd_obj.communicate()[0].decode("utf-8").split('\n')

    try:
        for l in output:
            if re.search('^ID_LIKE',l):
                res = l.replace('"','').split('=')
                return res[1]
    except Exception as e:
        return str(e)
            
""" Executa comando """
def run_cmd(cmd,msg):
    
    print("{} ".format(msg),end='',flush=True)
    set_log('info','{}'.format(msg))
    
    cmd_obj = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    output = cmd_obj.communicate()[0].decode("utf-8")
    rc = cmd_obj.returncode
    
    if cmd == 'exit 1':
        sys.exit(1)

    if rc != 0:
        set_log('error',output)
        print("OK",flush=True)
    else:
        set_log('success',msg)
        print("FAIL",flush=True)


""" Install Docker """
def install_docker():
    
    print("Instalando Docker... ",end='',flush=True)
    
    # set log
    set_log('info','Iniciando instalacao do Docker')

    # Get linux distro
    id_like = get_distro()
    
    # configura comando conforme distro
    if re.search('debian', id_like, re.IGNORECASE):
        cmd = 'curl https://get.docker.com | sh'
        msg = 'Install Docker'
        
    elif re.search('rhel',id_like, re.IGNORECASE):
        cmd = 'curl https://get.docker.com | sh'
        msg = 'Install Docker'

    else:
        cmd = 'exit 1'
        msg = 'Install Docker'
        print("FAIL",flush=True)
        set_log('error','Sistema Operacional nao suportado.')

    if run_cmd(cmd,msg):
        print("OK",flush=True)
    else:
        print("FAIL",flush=True)
        sys.exit(1)


    # Iniciando docker
    print("Iniciando docker... ",end='',flush=True)
    set_log('info','Iniciando docker')
    msg = 'Iniciando docker-compose'
    cmd = 'systemctl enable docker ; systemctl start docker'
    if run_cmd(cmd,msg):
        print("OK",flush=True)
    else:
        print("FAIL",flush=True)


""" Instala o docker compose """
def install_docker_compose():
    
    msg = 'Install docker-compose'
    cmd = 'sudo curl -s -L "https://github.com/docker/compose/releases/download/1.28.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/bin/docker-compose'
    print("{}...".format(msg),end='',flush=True)
    set_log('info','{}'.format(msg))

    if run_cmd(cmd,msg):
        print("OK",flush=True)
    else:
        print("FAIL",flush=True)
    
    # Ajusta permissão do arquivo
    msg = 'Configurando docker-compose'
    cmd = 'chmod +x /usr/bin/docker-compose'
    print("{}...".format(msg),end='',flush=True)
    set_log('info','{}'.format(msg))
    if run_cmd(cmd,msg):
        print("OK",flush=True)
    else:
        print("FAIL",flush=True)
    

""" Inicia o build """
def build():
    
    cmd = 'docker-compose build'
    msg = 'Realizando o build das imagens...'
    print("{} ".format(msg),end='',flush=True)
    set_log('info','{}'.format(msg))
    if run_cmd(cmd,msg):
        print("OK",flush=True)
    else:
        print("FAIL",flush=True)

""" Inicia os containers """
def start_containers():
    
    cmd = 'docker-compose --env-file .env up -d'
    msg = 'Iniciando containers... '
    print("{} ".format(msg),end='',flush=True)
    set_log('info','{}'.format(msg))
    if run_cmd(cmd,msg):
        print("OK",flush=True)
    else:
        print("FAIL",flush=True)


# Inicia instalacao
install_docker()
install_docker_compose()
build()
start_containers()


