FROM postgres:9.6

#RUN sed -i "s/CHANGE_DB_PASSWORD/$POSTGRES_PASSWORD/g" /docker-entrypoint-initdb.d/netbox_config.sql 
RUN ls -l docker-entrypoint-initdb.d/