# shiori

*Note: this script is written for python3.*

Example Usage to send to a MongoDB backend:
```bash
python ./shiori/shiori.py --load-covers --export-opts "mongo_uri=mongodb://<username>:<password>@qwerwrt-shard-00-00-b5hdc.mongodb.net:27017/test?ssl=true&replicaSet=qwetewq-shard-0&authSource=admin,mongo_db=wqerweq,mongo_collection=werweq" ./Songs mongo
```
Any errors found during the scraping process is outputted to a log file.

### Using the `docker-compose` version of azunyan
Note that if you are using the `docker-compose` version of azunyan you will need to first create an SSH tunnel into the docker network with the command
```bash
ssh -o StrictHostKeyChecking=no -p 2222 -L 27017:database:27017 linuxserver.io@<server_address>
```
you can then run Shiori as above with the command
```bash
python ./shiori/shiori.py --load-covers --export-opts "mongo_uri=mongodb://localhost:27017,mongo_db=azunyan,mongo_collection=songs" ./Songs mongo
```

### Using Powershell on Windows
Note if using Powershell you may need to set it to use UTF-8 explicity so it prints out the unicode characters
correctly in the console. The following command does this

```powershell
$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding =
                    New-Object System.Text.UTF8Encoding
```

To persist these settings, i.e. to make your future interactive PowerShell sessions UTF-8-aware by default, add the command above to your `$PROFILE ` file.

