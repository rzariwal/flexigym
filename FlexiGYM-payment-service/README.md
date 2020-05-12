# flexigym-payment-service



### using Docker to containerize springboot application minimal
```
cd payment-service
docker build -t payment:1.0 .
docker run -d -p 8080:8080 payment:1.0
```

```
│   ├── FlexiGYM-payment-service
│   │   ├── README.md
│   │   └── payment-service
│   │       ├── Dockerfile
│   │       ├── kubernetes
│   │       │   ├── payment-api-deployment.yaml
│   │       │   └── payment-api-service.yaml
│   │       ├── kustomization.yml
│   │       ├── mvnw
│   │       ├── mvnw.cmd
│   │       ├── out
│   │       │   └── production
│   │       ├── pom.xml
│   │       ├── src
│   │           ├── main
│   │           └── test
```
