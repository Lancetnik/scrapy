BOT_NAME = 'crawlers'

SPIDER_MODULES = ['crawlers.spiders']
NEWSPIDER_MODULE = 'crawlers.spiders'

FEED_EXPORT_ENCODING = 'utf-8'

ROBOTSTXT_OBEY = True

DOWNLOAD_FAIL_ON_DATALOSS = False

LOG_ENABLED = False

ITEM_PIPELINES = {
   'crawlers.pipelines.PostgresPipeline': 100,
}