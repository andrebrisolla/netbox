# Configura  arquivo 'configuration.py'
SECRET_KEY=$(date | sha256sum | awk '{print $1}' )
cat /tmp/configuration.py | \
    sed  "s/NETBOX_DB_CHANGE_PASSWORD/$NETBOX_PASSWORD/g;s/NETBOX_DB_CHANGE_SECRET_KEY/$SECRET_KEY/g" \
    > /opt/netbox/netbox/netbox/configuration.py

# Aguarda o banco subir para iniciar as configurações da aplicação
PSQL="psql -U postgres -h netbox_db password=$POSTGRES_PASSWORD -e"
$( echo "\l" | $PSQL > /dev/null 2> /dev/null )
while [ $( echo "\l" | $PSQL > /dev/null 2> /dev/null ; echo $? ) != 0 ]
do
        echo 'Aguardando a subida do banco...'
        sleep 2
done

echo "Banco no ar."
echo

# Roda o database migration
python3 /opt/netbox/netbox/manage.py migrate

# Cria o usuario admin
python3 /opt/netbox/netbox/create_superuser.py

# Adiciona os arquivos estáticos 
python3 /opt/netbox/netbox/manage.py collectstatic --noinput

# Update Netbox
/opt/netbox/upgrade.sh

# Inicia o serviço
echo -ne "\n### INICIANDO NETBOX ###\n"
python3 /opt/netbox/netbox/manage.py runserver 0.0.0.0:8000 --insecure