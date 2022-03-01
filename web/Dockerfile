FROM nginx:stable-alpine

RUN apk add --update npm
COPY ./default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
WORKDIR /web

RUN npm install
CMD ["nginx", "-g", "daemon off;"]
