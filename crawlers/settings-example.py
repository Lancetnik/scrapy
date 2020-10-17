BOT_NAME = 'crawlers'

SPIDER_MODULES = ['crawlers.spiders']
NEWSPIDER_MODULE = 'crawlers.spiders'

FEED_EXPORT_ENCODING = 'utf-8'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'crawlers.pipelines.PostgresPipeline': 100,
}

DB_HOST = ''
DB_PORT = '5432'
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''