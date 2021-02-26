FROM centos:7

# Instala pacotes
RUN yum install -y gcc python34 python34-devel python34-setuptools \
                    libxml2-devel libxslt-devel libffi-devel graphviz \
                    openssl-devel redhat-rpm-config git python3-pip postgresql

# Download do netbox
RUN cd /opt && git clone -b master https://github.com/digitalocean/netbox.git

# Configuração do Netbox
RUN useradd netbox
RUN chown -R netbox:netbox /opt/netbox/ 
RUN pip3 install --upgrade pip
RUN pip3 install napalm pipenv
RUN pip3 install -r /opt/netbox/requirements.txt

# Copia arquivos necessários para a instalação/configuração do ambiente
COPY ./config/configuration.py /tmp/configuration.py
COPY ./config/create_superuser.py /opt/netbox/netbox/create_superuser.py

# Inicia a configuração e a aplicação
CMD sh /docker-entrypoint/init.sh
