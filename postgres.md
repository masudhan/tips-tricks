### Check running quries with client address

`select pid, query, age(current_timestamp, query_start) as age, client_addr
from pg_stat_activity
where age(current_timestamp, query_start) is not null
order by age desc;`

### Install postgres in docker

`docker pull postgres:13.12`

`docker run --name pgsql -e POSTGRES_PASSWORD=<password> -p 5432:5432 postgres:13.12`

`docker exec -it pgsql bash`

Inside the container - `psql -h localhost -U postgres`
