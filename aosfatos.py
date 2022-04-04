import scrapy


class AosFatosSpider(scrapy.Spider):
    name = 'aos_fatos'

    start_urls = ['https://www.aosfatos.org/']

    def parse(self, response, **kwargs):
        links = response.xpath('//nav//ul//li//a[re:test(@href, "checamos")]/@href').getall()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_category
            )
    def parse_category(self, response):
        news = response.css('a[class^=entry]::attr(href)').getall()
        for new_url in news:
            yield scrapy.Request(
                response.urljoin(new_url),
                callback=self.parse_new
            )
        page_url = response.css('.pagination a::attr(href)').getall()
        for page in page_url:
            yield scrapy.Request(
                response.urljoin(page),
                callback=self.parse_category,
            )

    def parse_new(self,response):
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
                # 'quotes': quotes
                'quote_text': quote_text,
                'status': status,
                'image_stamp': 'https://www.aosfatos.org/' + image_stamp
            }

