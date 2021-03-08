#!/bin/bash
# Autor: André Müzel Brisolla
# Data: Mar 03, 2021
# Objetivo: Realizar um deploy do Netbox num ambiente containerizado.
# Prereqs: git

# Colors
Color_Off='\033[0m'       # Off
IRed='\033[0;91m'         # Red
IGreen='\033[0;92m'       # Green
IWhite='\033[0;97m'       # White

# Configura log
LOG_FILE="/tmp/netbox_install.log"
function set_log() {

    msg=$1
    echo -ne "\t$msg\r"
    date_time=$( date "+%d/%m/%Y, %H:%M:%S" )
    echo "$date_time : $msg" >> $LOG_FILE

}

# Verifica execução do comando
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

# Instala o Docker
function install_docker() {

    set_log "Instalando Docker"    
    curl -s  https://get.docker.com | bash 2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?

}

# Habilita o serviço do Docker
function config_docker() {

    set_log "Configurando serviço do Docker"
    systemctl enable docker  2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?

}

# Inicia o Docker
function start_docker() {

    set_log "Iniciando serviço do Docker"
    systemctl start docker  2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?

}

# Instala o Docker Compose
function install_docker_compose() {

    set_log "Instalando Docker Compose"
    curl -s -L "https://github.com/docker/compose/releases/download/1.28.4/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/bin/docker-compose | \
        bash 2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?

}

# Configura permissões do Docker Compose
function configura_docker_compose() {

    set_log "Configurando Docker Compose"
    chmod +x /usr/bin/docker-compose
    check_cmd $?

}

# Realiza o build das imagens
function build() {
    
    set_log "Iniciando o build"
    /usr/bin/docker-compose build 2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?

}

# Inicia os containers
function start_containers() {
    
    set_log "Iniciando os containers"
    /usr/bin/docker-compose --env-file .env up -d 2>> $LOG_FILE >> $LOG_FILE
    check_cmd $?
    
}

# Exibe uma mensagem ao final da instalação
function message() {

    IP=($( hostname -i | sed 's/ /\n/g' | grep -v ^127  ))

    echo -ne "\n$IGreen Instalação do Netbox concluida com sucesso!\n $Color_Off"
    echo -ne "\n Acesso Netbox:\n"
    for a in ${IP[@]}
    do
        echo -ne "   - http://$a/\n"
    done

    echo -ne "\n Acesso ao painel de Backup do Banco de Dados:\n"
    for a in ${IP[@]}
    do
        echo -ne "   - http://$a/backup_webapp/\n"
    done

    source .env
    echo -ne "\n Dados de acesso:"
    echo -ne "\n   - Netbox: $IRed admin/${NETBOX_PASSWORD} $Color_Off"
    echo -ne "\n   - Painel de Backup: $IRed postgres/${POSTGRES_PASSWORD}  $Color_Off\n\n\n"

}

function help() {
    echo -ne "\n  install.sh - Instalador do Netbox\n\n"
    echo -ne "\t--all  : Instalao Docker, Docker Compose, \n\t         realiza o build das imagens e inicia os containers.\n\n"
    echo -ne "\t--build : Realiza o build das imagens e inicia os containers.\n\n\n"
}

case $1 in
    --all)
        install_docker
        config_docker
        start_docker
        install_docker_compose
        configura_docker_compose
        build
        start_containers
        message
    ;;
    --build)
        build
        start_containers
        message
    ;;
    *)
        help
    ;;
esac
