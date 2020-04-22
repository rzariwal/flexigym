# flexigym-sms-notification-api

http://34.87.6.16:7000/api/docs/

cd /C/Users/sande/PycharmProjects/FlexiGYM-Notification-API

docker-compose -f docker-compose.yml up --build

docker ps 

docker logs flexigym-sms-notification-api_flexigym_notification_api_db_1

docker exec -it flexigym-sms-notification-api_flexigym_notification_api_db_1 mysql -u root -p

docker exec -it flexigym-sms-notification-api_flexigym_notification_api_db_1 bash 

docker container ls -a

docker container rm e0cc1df29223 

 docker kill $(docker ps -q) # stop all containers
 docker rm $(docker ps -a -q) # remove all containers 
 docker rmi $(docker images -q) # remove all images
 docker network prune # remove all networks
 docker volume prune # remove all volumes 
