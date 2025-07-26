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
How to add new replicaset?
  In primary,
    rs.add("172.16.16.250:27017")
    rs.printSlaveReplicationInfo()

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

https://www.mongodb.com/docs/v4.2/tutorial/force-member-to-be-primary/

var data = JSON.parse(cat('local json file name'));

data = data.map(doc = {
    if (doc._id && doc._id.$oid) {
        doc._id = ObjectId(doc._id.$oid);
    }
    return doc;
});

db.collectionName.insertMany(data);

-----------------------------------------------

mongo dump and restore

nohup mongodump --uri "mongodb://username:password@hostname:27017/?authSource=db&tls=true" \
          --collection dummy_cv_do_not_use_1_1_0 \
          --db dbname \
          --out /root/dump \
           /root/dump/dump.log 2&1 &

nohup mongodump --uri "mongodb://username:password@hostname:27017/dbname?authSource=dbname&tls=true" \
          --collection dummy_cv_do_not_use_1_1_0 \
          --out /root/madhu \
           /root/madhu/dump.log 2&1 &          