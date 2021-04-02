BOT_NAME = 'crawlers'

SPIDER_MODULES = ['crawlers.spiders']
NEWSPIDER_MODULE = 'crawlers.spiders'

FEED_EXPORT_ENCODING = 'utf-8'

ROBOTSTXT_OBEY = True

DOWNLOAD_FAIL_ON_DATALOSS = True

LOG_ENABLED = False

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'

ITEM_PIPELINES = {
   'crawlers.pipelines.PreprocessPipeline': 100,
   'crawlers.pipelines.PostgresPipeline': 200
}