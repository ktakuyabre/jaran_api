#jaran\_api

##Members<br />
Mizushima Shunto<br />
Kawai Takuya<br />

##Docker

Download Docker on your Mac or Windows : https://hub.docker.com/editions/community/docker-ce-desktop-mac (Mac), https://hub.docker.com/editions/community/docker-ce-desktop-windows (Windows)
Open Docker.


##Setup

```
$ docker-compose up
$ docker exec -i $(docker ps | grep postgres | awk '{print $1}') psql -U postgres -d postgres < db_data.sql
```

When you shut down jaran\_api

```
$ docker-compose down
```


##Usage

open url : http://localhost:8000/jaran_onsen


##Backup and restore database

Back up

```
$ docker exec $(docker ps | grep postgres | awk '{print $1}') pg_dump -U postgres postgres > db_data.sql
```

Restore
```
$ docker exec -i $(docker ps | grep postgres | awk '{print $1}') psql -U postgres -d postgres < db_data.sql
```

jaran\_get\_data.py
show help :
```
$ docker exec -i $(docker ps | grep jaran_api_web | awk '{print $1}') python3 jaran_get_data.py -h 
```
quick usage :
```
$ docker exec -i $(docker ps | grep jaran_api_web | awk '{print $1}') python3 jaran_get_data.py <yad-id>
```

rurubu\_get\_data.py
show help :
```
$ docker exec -i $(docker ps | grep jaran_api_web | awk '{print $1}') python3 rurubu_get_data.py -h 
```
quick usage :
```
$ docker exec -i $(docker ps | grep jaran_api_web | awk '{print $1}') python3 rurubu_get_data.py url 
```
