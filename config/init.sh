# Configura  arquivo 'configuration.py'
SECRET_KEY=$(date | sha256sum | awk '{print $1}' )
cat /tmp/configuration.py | \
    sed  "s/NETBOX_DB_CHANGE_PASSWORD/$POSTGRES_PASSWORD/g;s/NETBOX_DB_CHANGE_SECRET_KEY/$SECRET_KEY/g" \
    > /opt/netbox/netbox/netbox/configuration.py

# Roda o database migration
python3 /opt/netbox/netbox/manage.py migrate

# Cria o usuario admin
python3 /opt/netbox/netbox/create_superuser.py

# Adiciona os arquivos estáticos 
python3 /opt/netbox/netbox/manage.py collectstatic --noinput

# Inicia o serviço
echo "============= INICIANDO DJANGO =============="
python3 /opt/netbox/netbox/manage.py runserver 0.0.0.0:8000 --insecure