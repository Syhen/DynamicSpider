# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import six as _six
from scrapy.item import DictItem as _DictItem, ItemMeta as _ItemMeta


class _DynamicItem(_DictItem):
    """make a class of `scrapy.Item`"""

    def __init__(self, item_names):
        for name in item_names:
            self.fields[name] = None
        super(_DynamicItem, self).__init__()

    def __call__(self):
        return self


@_six.add_metaclass(_ItemMeta)
class ItemMaker(_DynamicItem):
    pass


if __name__ == '__main__':
    ItemClass = ItemMaker(['name', 'value', 'url'])
    item = ItemClass()
    item['name'] = 'heyao'
    item['value'] = 22
    item['url'] = 'https://github.com/syhen'
    pass
