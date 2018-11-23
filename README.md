# shiori

Note is using Powershell you may need to set it to use UTF-8 explicity so it prints out the unicode characters
correctly in the console. The following command does this

```powershell
$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding =
                    New-Object System.Text.UTF8Encoding
```

To persist these settings, i.e. to make your future interactive PowerShell sessions UTF-8-aware by default, add the command above to your `$PROFILE ` file.

Any errors found during the scraping process is outputted to a log file.