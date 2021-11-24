# playwright-turbo-collector
Playwright script which downloads registry files of persons performing medical activity 
from https://rpwdl.ezdrowie.gov.pl and saves them on s3 cloud.

Connection key must be dict type.
Optionally you can comment out line 36 ``` download.save_as(path=f"./{file_name}.zip") ```
to turn off saving files on your computer.




Libraries:
* Playwright 1.17.0
* minio 7.0.3

Python version - 3.8
