# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class DeDupePipeline(object):
    def __init__(self):
        self.email_addresses_seen = set()

    def process_item(self, item, spider):
        if item['email_address'] in self.email_addresses_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.email_addresses_seen.add(item['email_address'])
            return item
