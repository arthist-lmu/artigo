FROM nginx:stable-alpine

RUN apk add --update npm
COPY ./web/default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
WORKDIR /web

CMD ["nginx", "-g", "daemon off;"]
