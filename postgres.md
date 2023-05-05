### Check running quries with client address

`select pid, query, age(current_timestamp, query_start) as age, client_addr
from pg_stat_activity
where age(current_timestamp, query_start) is not null
order by age desc;`
