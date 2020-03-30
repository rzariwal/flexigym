FROM openjdk:8-jdk-alpine
ENV APP_FILE target/payment-service-1.0.0.jar
ENV APP_HOME /usr/app
COPY target/payment-service-1.0.0.jar /usr/app
WORKDIR $APP_HOME
ENTRYPOINT ["sh", "-c"]
CMD ["exec java -jar $APP_FILE"]
