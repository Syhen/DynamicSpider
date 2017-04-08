# DynamicSpider
## Description

A dynamic spider by scrapy. 

## Usage

Create a mongodb database named ``spider`` , create a collection named ``rules``. The rule format are just like this:

```json
{
  "_id": 8,
  "name": "创世中文网",
  "start_url": [
    "http://chuangshi.qq.com/bk/zp1gx3/"
  ],
  "next_page": "//a[@class=\"nextBtn\"]/@href",
  "body_list": "//div[@class=\"leftlist\"]/table/tr[not(@class)]",
  "meta": {
    "source": 8
  },
  "item_name": [
    "title",
    "author",
    "source"
  ],
  "xpath": {
    "title_xpath": "./td[3]/a[1]/text()",
    "author_xpath": "./td[5]/a/text()"
  }
}
```

run ``python run.py``.

## Updated

1. **#2017-04-08#init the project**: support basic dynamic crawl for list and next page.