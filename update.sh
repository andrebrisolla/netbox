#sudo rm -rf /var/lib/postgresql/data/
#sudo docker rm -f netbox_db netbox_app
sudo docker-compose build
sudo docker-compose --env-file .env up -d

