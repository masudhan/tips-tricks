### Check running quries with client address

`select pid, query, age(current_timestamp, query_start) as age, client_addr
from pg_stat_activity
where age(current_timestamp, query_start) is not null
order by age desc;`

### postgres on docker

`docker pull postgres:13.12`

`docker run --name pgsql -e POSTGRES_PASSWORD=<password> -p 5432:5432 postgres:13.12`

`docker exec -it pgsql bash`

Inside the container - `psql -h localhost -U postgres`


### pgAdmin4 on docker and connect to postgres

`docker pull dpage/pgadmin4`

`docker run -e 'PGADMIN_DEFAULT_EMAIL=madhu@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=<password>' -p 8080:80 --name pgadmin4 dpage/pgadmin4`

test in localhost:8080

`docker inspect pgsql` - get the IPAddress under Networks

Create new connection - give hostname/address from above IP and username and password accordingly

