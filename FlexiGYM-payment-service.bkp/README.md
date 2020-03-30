# flexigym-payment-service



### using Docker to containerize springboot application minimal
```
cd payment-service
docker build -t payment:1.0 .
docker run -d -p 8080:8080 payment:1.0
```
