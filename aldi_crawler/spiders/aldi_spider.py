import scrapy
import chompjs
import re
import json
from scrapy.linkextractors import LinkExtractor


class AldiGroceryItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    packsize = scrapy.Field()
    price = scrapy.Field()
    price_per_unit = scrapy.Field()
    category = scrapy.Field()
    # sub_category = scrapy.Field()


class AldiSpider(scrapy.Spider):
    name = "aldi"

    start_urls = [
        'https://www.aldi.com.au/en/groceries/'
    ]
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["category", "title", "packsize", "price", "price_per_unit", "image"]
    }

    def parse(self, response):
        filename = 'aldi_grocery.html'
        a_tags = response.xpath("//li[contains(@class,'tab-nav--item dropdown--list--item')]/a")
        
        for a in a_tags:
            href = a.xpath("@href").extract_first()
            yield response.follow(href, callback=self.get_product_details, meta = {'href': href})

    def get_product_details(self, response):
        products = response.xpath("//a[@title='to product detail']")
        category = str(response.meta['href']).replace("https://www.aldi.com.au/en/groceries/","")
        print(f"START scraping gorcery catergory {category}")

        if len(products) == 0:
            print("INFO: No Product Found. Try Next Sub-pages")

            a_tags = response.xpath("//div[contains(@class,'csc-textpic csc-textpic-left csc-textpic-above')]//div[contains(@class, 'csc-textpic-imagecolumn')]//a")
            
            if "liquor" in str(response.meta['href']):
                a_tags = response.xpath("//div[@id='c82805']//div[contains(@class,'csc-textpic csc-textpic-center csc-textpic-above ym-clearfix')]//div[contains(@class, 'csc-textpic-imagecolumn')]//a")

            for a in a_tags:
                href = a.xpath("@href").extract_first()
                # sub_category = a.xpath("@href").extract_first().replace("https://www.aldi.com.au/en/groceries/","").replace("/","")
                yield response.follow(href, callback=self.get_product_details, meta = {'href': href})

        # sub_category = ""
        # try:
        #     sub_category = str(response.meta['sub_category'])
        # except:
        #     print("No subcategory found")

        for product in products:

            item = AldiGroceryItem() 

            product_xpath = product.xpath("div//div")
            
            print("\n")
            print("PRODUCT DETAILS")

            product_title = product_xpath.xpath("div[@class='box--description--header']/text()").extract()
            product_title = list(map(lambda s: s.strip(), product_title))
            product_title = ' '.join(map(str, product_title)) 
            print(f"Product title: {product_title}")

            product_image = product_xpath.xpath("img/@src").extract_first().strip()
            print(f"Product image: {product_image}")

            product_package_size = ""
            try:
                product_package_size = product_xpath.xpath("span[@class='box--amount']/text()").extract_first().strip()
                print(f"Product package size: {product_package_size}")
            except:
                product_package_size = "N/A"
                print(f"Product package size: {product_package_size}")
            

            unit = ""

            try:
                _product_box_value = float(product_xpath.xpath("span[@class='box--value']/text()").extract()[0].strip().replace("$","").replace(".",""))
            except:
                _product_box_value = "N/A"
            

            try:
                unit = str(product_xpath.xpath("span[@class='box--value'][2]/text()").extract_first().strip())
            except:
                unit = "$"

            try:
                _product_box_decimal = float("0." + product_xpath.xpath("span[@class='box--decimal']/text()").extract_first().strip())
            except:
                print("Warning: Decimal in price is None")

            if unit == "c":
                product_price = str(_product_box_value) + str(unit)
                print(f"Product price: {str(product_price)}")
            else:
                if _product_box_value != "N/A":
                    product_price = _product_box_value + _product_box_decimal
                    print(f"Product price: {str(product_price)}")
                else:
                    print(f"Product price: N/A or see price in store")
            

            price_per_unit = ""
            try:
                price_per_unit = product_xpath.xpath("span[@class='box--baseprice']/text()").extract_first().strip()
                print(f"Price per unit: {price_per_unit}")
            except:
                price_per_unit = "N/A"
                print(f"Price per unit: {price_per_unit}")
           
            print("\n")

            item['title'] = product_title
            item['image'] = product_image
            item['packsize'] = product_package_size
            item['price'] = product_price
            item['price_per_unit'] = price_per_unit
            item['category'] = category
            # item['sub_category'] = sub_category

            yield item