#!/bin/bash

# Colors
Color_Off='\033[0m'
IRed='\033[0;91m'         # Red
IGreen='\033[0;92m'       # Green
IWhite='\033[0;97m'       # White


# configura log
LOG_FILE="/tmp/netbox_install.log"

function set_log() {

    msg=$1
    echo -ne "\t$msg\r"
    date_time=$( date "+%d/%m/%Y, %H:%M:%S" )
    echo "$date_time : $msg" >> $LOG_FILE

}

function check_cmd() {

    rc=$1

    if test $rc -eq 0
    then
        echo -ne $IGreen "ok $Color_Off\n"
    else
        echo -ne $IRed "fail $Color_Off\n"
        echo -ne "\n\t"
        exit
    fi

}

function install_docker() {

    set_log "Instalando Docker"    
    curl -s  https://get.docker.com | bash 2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?

}

function config_docker() {

    set_log "Configurando serviço do Docker"
    systemctl enable docker | bash 2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?

}

function start_docker() {

    set_log "Configurando serviço do Docker"
    systemctl start docker | bash 2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?

}

function install_docker_compose() {

    set_log "Instalando Docker Compose"
    sudo curl -L "https://github.com/docker/compose/releases/download/\1.28.4/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/bin/docker-compose | \
        bash 2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?

}

function configura_docker_compose() {

    set_log "Configurando Docker Compose"
    chmod +x /usr/bin/docker-compose
    check_cmd $?

}

install_docker
config_docker
start_docker
install_docker_compose
configura_docker_compose