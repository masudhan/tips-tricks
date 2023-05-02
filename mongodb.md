```
mongodump --host example.com --port 27017 --username myuser --password mypassword --out /path/to/dump_directory

mongorestore --host example.com --port 27017 --username myuser --password mypassword --authenticationDatabase admin /path/to/dump_directory

------------------------------------------------
How to force a member to be primary?

Let's say we have mongo-1 (primary), mongo-2 (secondary), mongo-3 (secondary)

I want to make mongo-3 as primary 

So get into mongo-2 (so that it does not attempt to become primary for 120 seconds)
  rs.slaveOk()
  rs.freeze(120)
  
Now get into mongo-1 which is primary (step down this instance that the mongod is not eligible to become primary for 120 seconds:)
  rs.stepDown(120)

Now if we get into mongo-3 it'll be primary

-------------------------------------------------
How to remove replicaset?
1. Get into secondary instances 
  use admin;
  rs.slaveOk()
  db.shutdownServer()
2. Get into primary instances
  use admin;
  rs.remove("172.16.16.200:27017")

```
