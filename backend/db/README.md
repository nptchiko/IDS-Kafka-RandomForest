# Docker-mongodb

Code for blog entry at: <a href="https://fabianlee.org/2018/05/20/docker-using-docker-compose-to-link-a-mongodb-server-and-client">https://fabianlee.org/2018/05/20/docker-using-docker-compose-to-link-a-mongodb-server-and-client</a>


### This is module contain MongoDB Database (Ubuntu)

Data from kafka consumer transfer to MongoDB. 
This databae run on docker.

You must be run this database before run websocket

## How to init database MongoDB

__Navigate here__

Let's make sure docker that use port 27017 not use.
```
docker down -v my-mongodb
```
Now follow this command.
```
docker compose up -d
```
Everything that OK.
Let's check database in mongosh

```
docker exec -it my-mongodb mongosh -u admin -p admin --authenticationDatabase admin
```
You login in database with admin

___Some command for check database___
```
show collections # Check all collection
db.<collection>.find().pretty() # Check all document in collection.
```