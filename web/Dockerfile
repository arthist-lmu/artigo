FROM nginx:stable-alpine

RUN apk add --update npm
COPY ./web/default.conf /etc/nginx/conf.d/default.conf
COPY ./plugin.config.json /config.json
COPY ./web/ /web
WORKDIR /web
#RUN npm install --legacy-peer-deps && npm run build && npm prune --production
RUN npm update && npm run build && npm prune --production

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
