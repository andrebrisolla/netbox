import psycopg2,os,hashlib,datetime,stat,subprocess,time, humanfriendly,glob


class Backup():

    def __init__(self):
        pass


    def login(self,data):
        
        psql_pass = data['password']

        try:
            conn = psycopg2.connect(
                dbname="netbox", 
                user="postgres", 
                password=str(psql_pass),
                host='netbox_db'
                )
            
            # Cria token
            dt = str(datetime.datetime.now())
            token = hashlib.md5(dt.encode('utf-8')).hexdigest()

            # Inclui o hash num arquivo de "sessao"
            session_file = open('/tmp/session_file.txt','a')
            session_file.write('{}|{}\n'.format(token,dt))
            
            # Retorna informações de login
            return {
                'code' : 200,
                'token' : token
            }



        except Exception as e:
            return {
                'code' : 403,
                'message' : 'Erro no login. Verifique o usuário e senha.'
            }
        

    def login_check(self,data):
        

        try:
            # Get token
            token = data['token']
            
            # get session file
            session_file = open('/tmp/session_file.txt','r')

            # fins tokens insession file
            tokens = []
            for line in session_file.readlines():
                tmp = line.split("|")
                tk = tmp[0]
                tokens.append(tk)
            
            if token in tokens:
                return {
                    'code' : 200
                }
            else:
                return {
                    'code' : 403,
                    'message' : 'Acesso negado!'
                }
        
        except Exception as e:
            return {
                    'code' : 403,
                    'message' : 'Acesso negado!'
            }


    def create_backup(self):
        
        try:
            # get postgres password
            psql_pass = os.environ['POSTGRES_PASSWORD']
            os.environ['PGPASSWORD'] = psql_pass

            # get datetime
            dt = datetime.datetime.now()
            dt_formated = dt.strftime('%Y%m%d_%H%M%S')
            
            # Create postgresql connection file
            pgsql_config = 'netbox_db:5432:netbox:postgres:{}'.format(psql_pass)
            pgpass = open('/root/.pgpass','w')
            pgpass.write(pgsql_config)
            os.chmod('/root/.pgpass', 0o600)
            
            # configure backup
            pg_dump_file = '/pg_dumps/netbox_dump_{}.sql'.format(dt_formated)
            pg_dump = 'pg_dump -Fp -U postgres -h netbox_db -f /pg_dumps/netbox_dump_{}.sql  netbox'.format(dt_formated)            

            

            # configure log
            dump_to = open(pg_dump_file,'a')
            log_file = open('/pg_dumps/dumps.log','a')

            # Execute backup
            run = subprocess.Popen(pg_dump, shell=True, stdout=dump_to, stderr=log_file)
            wait = run.communicate()[0]
            rc = run.returncode
            
            if rc == 0:
                return {
                    'code' : 200,
                    'message' : 'Backup realizado com sucesso!',
                    'file'  : pg_dump_file
                }
            else:
                return {
                    'code' : 500,
                    'message' : 'Erro ao realizar o backup!'
                }

        except Exception as e:
            return {
                    'code' : 500,
                    'message' : str(e)
                }
    

    def backup_delete(self,data):
        try:
            
            file = data['file']
            os.remove('/pg_dumps/{}'.format(file))

            return {
                'code' : 200,
                'message' : 'Backup removido com sucesso!'
            }


        except Exception as e:
            return {
                    'code' : 500,
                    'message' : str(e)
                }
    
    def backup_list(self):
        
        try:
            list_dumps = []
            files = glob.glob("/pg_dumps/*.sql")
            files.sort(key=os.path.getmtime, reverse=True)

            #for file in os.listdir(dump_dir):
            for file in files:
                if file.endswith(".sql"):
                    
                    #  get size
                    file_info = os.stat(file)
                    file_size = file_info.st_size
                    h_file_size = str(humanfriendly.format_size(file_size))

                    mtime = datetime.datetime.fromtimestamp(file_info.st_mtime)
                    mtime = mtime.strftime('%b %d, %Y - %H:%M:%S')
                    
                    list_dumps.append({
                        'file_name' : file.replace('/pg_dumps/',''),
                        'file_mtime' : mtime,
                        'file_size' : h_file_size
                    })
            
            return {
                'code' : 200,
                'data' : list_dumps
            }
        except Exception as e:
            return {
                'code' : 500,
                'message' : str(e)
            }


    def backup_restore(self,data):
        try:


            file_name = data['file']

            # get postgres password
            psql_pass = os.environ['POSTGRES_PASSWORD']
            os.environ['PGPASSWORD'] = psql_pass
                      
            # Create postgresql connection file
            pgsql_config = 'netbox_db:5432:netbox:postgres:{}'.format(psql_pass)
            pgpass = open('/root/.pgpass','w')
            pgpass.write(pgsql_config)
            os.chmod('/root/.pgpass', 0o600)
            
            # Remove database
            
            drop_script = open('/tmp/drop_script.sql','w')
            drop_script.write('REVOKE CONNECT ON DATABASE netbox FROM PUBLIC;\n')
            drop_script.write("SELECT pg_terminate_backend(pid) FROM  pg_stat_activity WHERE pid <> pg_backend_pid() AND datname = 'netbox'; \n")
            drop_script.write('DROP DATABASE netbox;\n')
            drop_script.write('CREATE DATABASE netbox;\n')
            drop_script.write('GRANT ALL PRIVILEGES ON DATABASE netbox TO netbox;\n')
            drop_script.close()
            pg_drop = 'psql -U postgres -h netbox_db < /tmp/drop_script.sql'

            try:
                ###### -> psql -U postgres -h netbox_db -Fp netbox < netbox_dump_20210303_202345.sql
                dump_log = open('/pg_dumps/dumps.log','a')
                

                # Dropa o Banco de dados e cria novamente
                run = subprocess.Popen(pg_drop, shell=True, stdout=dump_log, stderr=dump_log)
                wait = run.communicate()[0]
                rc = run.returncode

                # Executa o restore
                pg_restore = 'psql -U postgres -h netbox_db -Fp netbox < /pg_dumps/{}'.format(file_name)
                run = subprocess.Popen(pg_restore, shell=True, stdout=dump_log, stderr=dump_log)
                wait = run.communicate()[0]
                rc = run.returncode
                dump_log.close()

                return {
                    'code'  : 200,
                    'message' : 'Banco restaurado com sucesso!'
                }
            except Exception as e:
                return {
                    'code' : 500,
                    'message': str(e)
                }
            
        except Exception as e:
            return {
                'code' : 500,
                'message': str(e)
            }