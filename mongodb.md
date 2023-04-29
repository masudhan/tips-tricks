```
mongodump --host example.com --port 27017 --username myuser --password mypassword --out /path/to/dump_directory


mongorestore --host example.com --port 27017 --username myuser --password mypassword --authenticationDatabase admin /path/to/dump_directory
```
