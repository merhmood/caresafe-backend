#!/bin/bash

create_postgres_container="sudo docker run -d --name postgres-container -e POSTGRES_DB=mydatabase -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -p 5432:5432 postgres"

start_postgres_container="sudo docker start postgres-container"

eval $create_postgres_container || echo -e "\n\ncontainer already exist, starting container..." && eval $start_postgres_container 