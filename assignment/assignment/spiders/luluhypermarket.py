import scrapy


class LuluhypermarketSpider(scrapy.Spider):
    name = 'luluhypermarket'
    allowed_domains = ['www.luluhypermarket.com']
    start_urls = [
        'https://www.luluhypermarket.com/en-ae/electronics',
    ]

    def parse(self, response):
        final_sub_category_links = []
        final_sub_category_titles = []

        # getting all sub category links
        subcategory_links = response.xpath('//div[@class="col-lg-2 col-md-3 col-auto"]')
        # getting all sub category titles
        subcategory_titles = response.xpath('//div[@class="img-caption"]/text()')
        
        for subcategory_link, subcategory_title in zip(subcategory_links, subcategory_titles):
            link = subcategory_link.xpath('.//a/@href').get()
            link = 'https://www.luluhypermarket.com/en-ae' + str(link)
            
            # processing all sub category links and titles
            final_sub_category_links.append(link)
            final_sub_category_titles.append(subcategory_title.get())

            # getting sub category all products
            yield scrapy.Request(link, callback=self.parse_product)
            
        print(f"\nfinal-all-sub-category-links: {final_sub_category_links}\n")
        print(f"\nfinal-all-sub-category-titles: {final_sub_category_titles}\n")    

    def parse_product(self, response):
        # title = response.xpath('//h1[@class="product-title"]/text()').get()
        # price = response.xpath('//span[@class="product-price"]/text()').get()
        # yield {'title': title, 'price': price}
        print(response)
