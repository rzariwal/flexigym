FROM node:13.3.0 AS compile-image

RUN npm install

WORKDIR /opt/ng
COPY .npmrc package.json
RUN npm install

ENV PATH="./node_modules/.bin:$PATH"

COPY . ./
RUN ng build --prod

FROM nginx
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=compile-image /opt/ng/dist/web-front /usr/share/nginx/html
