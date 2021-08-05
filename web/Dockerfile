FROM nginx:1.16.1-alpine

RUN apk add --update npm
COPY ./default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
WORKDIR /web

CMD ["nginx", "-g", "daemon off;"]
