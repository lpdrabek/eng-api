FROM nginx

ADD eng_api.conf /etc/nginx/conf.d/
RUN rm -f /etc/nginx/conf.d/default.conf

RUN mkdir /log/
RUN touch /log/nginx-access.log
RUN touch /log/nginx-error.log

CMD ["nginx", "-g", "daemon off;"]
