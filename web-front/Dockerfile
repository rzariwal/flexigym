### STAGE 1: Build ###
FROM node:13.3.0-alpine AS build
WORKDIR /app
COPY package.json ./
RUN npm install
RUN npm audit fix
COPY . .
RUN npm run build


### STAGE 2: Run ###
FROM nginx:1.17.1-alpine
COPY --from=build /app/dist/web-front /usr/share/nginx/html

