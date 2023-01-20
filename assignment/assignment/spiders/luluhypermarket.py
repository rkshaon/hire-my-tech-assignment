import scrapy
from scrapy.exporters import JsonItemExporter


class LuluhypermarketSpider(scrapy.Spider):
    name = 'luluhypermarket'
    allowed_domains = ['www.luluhypermarket.com']
    start_urls = [
        'https://www.luluhypermarket.com/en-ae/electronics',
    ]

    def __init__(self):
        self.items = []

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


    def parse_product(self, response):
        final_product_links = []
        
        try:
            # getting all products under a sub category
            product_links = response.xpath('//div[@class="product-box js-gtmGA4-selct_item prevent-child-click"]')

            for product_link in product_links:
                link = product_link.xpath('./@data-url').get()

                # processing all products link
                link = 'https://www.luluhypermarket.com' + str(link)
                final_product_links.append(link)

        except Exception as e:
            print('\nError: ', str(e))
        
        # getting all product details
        for link in final_product_links:
            yield scrapy.Request(link, callback=self.parse_product_details)


    def parse_product_details(self, response):
        product_details = {}

        title = response.xpath('//h1[@class="product-name"]/text()').get()
        current_price = response.xpath('//span[@class="item price"]')
        currency = current_price.xpath('.//small/text()').get()
        value = current_price.xpath('.//span/text()').get()

        price = f"{currency} {value}"       

        product_summaries = response.xpath('//div[@class="description-block mb-3 mt-md-0"]')
        
        product_summary_list = []
        
        for li in product_summaries.xpath('.//ul/li'):
            product_summary_list.append(li.xpath('./text()').get())
        
        product_details['title'] = title
        product_details['price'] = price
        product_details['summary'] = product_summary_list

        # print(f"\n{product_details}")
    

    def closed(self, reason):
        # open the file for writing
        file = open('luluhypermarket.json', 'wb')
        # create an instance of JsonItemExporter
        exporter = JsonItemExporter(file)
        # start the export process
        exporter.start_exporting()
        # export the data
        exporter.export_items(self.items)
        # finish the export process
        exporter.finish_exporting()
        # close the file
        file.close()