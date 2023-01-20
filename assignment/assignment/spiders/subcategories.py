import scrapy

class SubcategorySpider(scrapy.Spider):
    name = "subcategories"
    start_urls = [
        'https://www.luluhypermarket.com/en-ae/electronics',
    ]

    def parse(self, response):
        subcategories_list = response.css('span.yCmsComponent nav__link js_nav__link')
        # subcategory_links = response.xpath('//div[@class="sub-category-list"]//a/@href').getall()
        # for link in subcategory_links:
        #     yield response.follow(link, self.parse_subcategory)

    # def parse_subcategory(self, response):
    #     subcategory_name = response.xpath('//h1[@class="category-title"]/text()').get()
    #     print(f"\n\nHere is my sub categories list: \n{subcategory_name}\n\n")
