#jaran_api


##Docker

Download Docker on your Mac. : https://hub.docker.com/editions/community/docker-ce-desktop-mac 
Open Docker.


##Setup

```
$ docker-compose up
$ docker exec -i $(docker ps | grep postgres | awk '{print $1}') psql -U postgres -d postgres < db_data.sql
```

When you shut down jaran_api

```
$ docker-compose down
```


##Usage

open url : http://localhost:8000/jaran_onsen


##Backup and restore database

Back up

```
$ docker exec -i $(docker ps | grep postgres | awk '{print $1}') pgdump -U postgres postgres > db_data.sql
```

Restore
```
$ docker exec -i $(docker ps | grep postgres | awk '{print $1}') psql -U postgres -d postgres < db_data.sql
```
