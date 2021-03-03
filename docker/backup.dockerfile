FROM python:latest

RUN apt update && apt install postgresql -y

RUN pip3 install Flask Flask-Caching Flask-Cors psycopg2 humanfriendly

CMD export FLASK_APP=/app/app.py ; \
    export FLASK_ENV=development ; \
    export FLASK_DEBUG=1 ; \
    flask run --host 0.0.0.0
