FROM docker/compose

WORKDIR /srv

COPY . .

CMD docker-compose up --build