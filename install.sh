#!/bin/bash


check_cmd() {

    rc=$1

    if test $rc -eq 1
    then
        echo "ok"
    else
        echo "nok"
    fi

}

install_docker() {

    curl -s  https://get.docker.com | bash #2> /dev/null > /dev/null
    check_cmd $?

}

install_docker