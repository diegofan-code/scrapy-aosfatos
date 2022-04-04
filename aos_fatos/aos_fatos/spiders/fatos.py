import scrapy
import w3lib.html
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

#import os; os._exit(0) # Sair do pdb quando ele roda junto com crawl scrapy

class FatosSpider(CrawlSpider):
    name = 'fatos'
    allowed_domains = ['aosfatos.org']
    start_urls = ['https://aosfatos.org/']

    rules = (
        Rule(
            LinkExtractor(
                restrict_css=(
                    'ul li a[href*="checamos"]')
            )
        ),
        Rule(
            LinkExtractor(
                restrict_css=('.pagination a')
            )
        ),
        Rule(
            LinkExtractor(
                restrict_css=(
                    'a[class^=entry]')
            ),
            callback='parse_new'
        ),
    )

    def parse_new(self, response):
        title = response.css('article h1::text').get()
        date = ' '.join(response.css('.publish-date::text').get().split())
        quotes = response.css('article blockquote')
        for quote in quotes:
            quote_text = quote.css('::text').get()
            status = quote.xpath('./preceding-sibling::p[1]/img/@data-image-id').get().replace('.png', '')
            if not status:
                continue
            image_stamp = quote.xpath('./preceding-sibling::p[1]/img/@src').get()
        
            yield {
                'title': title,
                'date': date,
                'url': response.url,
                'quote_text': quote_text,
                'status': status,
                'image_stamp': 'https://www.aosfatos.org/' + image_stamp
            }

