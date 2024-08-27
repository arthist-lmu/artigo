FROM nginx:1.25-alpine

ARG VUE_APP_API
ENV VITE_APP_API=$VUE_APP_API

RUN apk add --update npm

COPY /web/default.conf /etc/nginx/conf.d/default.conf
COPY /plugin.config.json /config.json
COPY /web /web/

EXPOSE 80
WORKDIR /web

RUN npm update && npm run build && npm prune --production

CMD ["nginx", "-g", "daemon off;"]
