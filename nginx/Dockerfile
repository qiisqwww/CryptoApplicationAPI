FROM nginx:1.23.3-alpine

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/
COPY ./trading_analyze_api.crt /etc/nginx
COPY ./trading_analyze_api.key /etc/nginx

CMD ["nginx", "-g", "daemon off;"]