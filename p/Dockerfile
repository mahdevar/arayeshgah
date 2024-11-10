FROM alpine
EXPOSE 5432

ENV PGDATA=/var/lib/postgresql/data
#VOLUME DATA=/var/lib/postgresql/data
RUN apk add postgresql postgresql-contrib

#RUN mkdir /run/postgresql/
#RUN chown -R postgres:postgres /run/postgresql/

USER postgres
#RUN mkdir $PGDATA
#RUN chown -R postgres /var/lib/postgresql/data

RUN initdb
COPY data $PGDATA
#RUN pg_ctl start

#RUN psql -U postgres -d postgres -c 'create user root'
#RUN createuser --superuser root
#RUN pg_ctl stop
#RUN psql -d postgres --command "create user root";
# createuser --superuser root
CMD ["postgres"]