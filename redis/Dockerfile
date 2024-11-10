FROM alpine
EXPOSE 6379
RUN apk update
RUN apk upgrade
RUN apk add redis
COPY redis.conf /etc/redis/redis.conf
CMD ["redis-server", "/etc/redis/redis.conf"]