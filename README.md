# Setup scrapy
1. Install python3,  python3-dev, python3-pip
2. Install scrapy, psycopg2, loguru, bs4 or use `pip3 install -r requirements.txt`
3. Create from crawlers/settings-example.py => crawlers/settings.py with yours DB settings 
4. From the repository's root run `scrapy crawl habr`

Optionally you can also use `scrapy crawl habr --output=data.json` for writing result to data.json file
or `scrapy crawl habr -L WARNING` to ignore scrapy debug messages.
Also, one can run this script from `cron` for 24/7 monitoring.


# Setup website
1. Install python3,  python3-dev, python3-pip
2. Install psycopg2, loguru, django, djangorestframework, django-filter or use `pip3 install -r requirements.txt`
3. Create from website/config/settings-example.py => website/config/settings.py with yours DB settings 
4. From the website/ run `python manage.py migrate` and `python manage.py runserver`