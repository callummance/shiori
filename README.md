# shiori

Example Usage to send to a MongoDB backend:
```bash
python ./shiori/shiori.py --load-covers --export-opts "mongo_uri=mongodb://<username>:<password>@qwerwrt-shard-00-00-b5hdc.mongodb.net:27017/test?ssl=true&replicaSet=qwetewq-shard-0&authSource=admin,mongo_db=wqerweq,mongo_collection=werweq" ./Songs mongo
```

Note if using Powershell you may need to set it to use UTF-8 explicity so it prints out the unicode characters
correctly in the console. The following command does this

```powershell
$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding =
                    New-Object System.Text.UTF8Encoding
```

To persist these settings, i.e. to make your future interactive PowerShell sessions UTF-8-aware by default, add the command above to your `$PROFILE ` file.

Any errors found during the scraping process is outputted to a log file.