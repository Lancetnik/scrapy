BOT_NAME = 'test_proj'

SPIDER_MODULES = ['test_proj.spiders']
NEWSPIDER_MODULE = 'test_proj.spiders'

FEED_EXPORT_ENCODING = 'utf-8'

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   'test_proj.pipelines.PostgresPipeline': 100,
}

DB_HOST = ''
DB_PORT = '5432'
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''