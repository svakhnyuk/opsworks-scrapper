# -*- coding: utf-8 -*-
import json
import random
import scrapy
import requests
import jmespath
from scrapy.spiders import CrawlSpider

class TargetItem(scrapy.Item):
    """
    Target items list
    """
    product_title = scrapy.Field()
    product_price = scrapy.Field()
    product_images = scrapy.Field()
    product_description = scrapy.Field()
    product_highlights = scrapy.Field()
    last_question = scrapy.Field()
    last_answer_asked = scrapy.Field()

class TargetSpider(CrawlSpider):
    """
    carwler to site target.com
    """
    name = 'target'
    allowed_domains = ['target.com']
    used_proxy_addresses = []
    crawling_url = 'https://www.target.com/p/consumer-cellular-apple-iphone-xr-64gb-black/-/A-81406260#lnk=sametab'
    count_proxy_changing = 0
    max_proxy_changing = 30

    def start_requests(self):
        """
        Start parse
        :param response:
        :return:
        """
        yield scrapy.Request(self.crawling_url, self.parse_target_page, dont_filter=True,
                             errback=self.error_achive_target)

    def parse_target_page(self, response):
        """
        Parse first_page
        :param response:
        :return:
        """
        item = TargetItem()
        self.response = response
        item['product_title'] = self.get_response_from_xpath('//*[@data-test="product-title"]//text()')

        url_request_json_details = self.get_url_request_json_details()
        request = scrapy.Request(url_request_json_details, callback=self.parse_target_page_details)
        request.meta['item'] = item
        yield request

        url_request_json_question = self.get_url_request_json_question()
        request = scrapy.Request(url_request_json_question, callback=self.parse_target_page_questions)
        request.meta['item'] = item
        yield request


    def parse_target_page_details(self, response):
        """
        Parse target page details
        :param: esponse
        :return:
        """
        item = response.meta['item']
        json_response = json.loads(response.text)
        product = jmespath.search('data.product', json_response)
        if product:
            item['product_price'] = self.get_product_price(product)
            item['product_images'] = self.get_product_images(product)
            item['product_description'] = self.get_product_description(product)
            item['product_highlights'] = self.get_product_highlights(product)

    def parse_target_page_questions(self, response):
        """
        Get target page questions
        :param: response
        :return: item
        """
        item = response.meta['item']
        json_response = json.loads(response.text)
        question_results = jmespath.search('results', json_response)
        if question_results and len(question_results) > 0:
            item['last_question'] = self.get_last_question(question_results[0])
            item['last_answer_asked'] = self.get_last_answer_asked(question_results[0])
        return item

    def get_url_request_json_details(self):
        """
        Get url for request json details
        :param:
        :return: JSON
        """
        script_window_tgt_data = self.get_script_by_key_variable('window.__TGT_DATA__')
        api_key = self.get_field_from_script_by_key('apiKey', script_window_tgt_data)
        tcin = self.get_field_from_script_by_key('tcin', script_window_tgt_data)
        pricing_store_id = self.get_field_from_script_by_key('pricing_store_id', script_window_tgt_data)
        if api_key and tcin and pricing_store_id:
            return f"https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1" \
                                  f"?key={api_key}&tcin={tcin}" \
                                  f"&store_id=none&has_store_id=false&pricing_store_id={pricing_store_id}" \
                                  f"&has_pricing_store_id=true" \
                                  f"&scheduled_delivery_store_id=none"

    def get_url_request_json_question(self):
        """
        Get url for request json question
        :param:
        :return: JSON
        """
        script_window_preloadad_state = self.get_script_by_key_variable('window.__PRELOADED_STATE__')
        questioned_id = self.get_field_from_script_by_key('"Product","tcin"', script_window_preloadad_state)
        api_key = self.get_field_from_script_by_key('"nova":{"apiKey":', script_window_preloadad_state)
        if api_key and questioned_id:
            return f"https://r2d2.target.com/ggc/Q&A/v1/question-answer?type=product" \
                                  f"&questionedId={questioned_id}&page=0&size=10&sortBy=MOST_ANSWERS&key={api_key}" \
                                  f"&errorTag=drax_domain_questions_api_error"

    def get_script_by_key_variable(self,key_variable):
        """
        Get text from script which contains key variable
        :param:
        :return: str
        """
        script_list = self.get_response_from_xpath_list('//script/text()')
        for script_content in script_list:
            if script_content.find(key_variable) >= 0:
                return script_content

    def get_field_from_script_by_key(self, key_word, script):
        """
        Get text from script with window.__TGT_DATA__ variable
        :param: str
        :return: str
        """
        if key_word and script and script.find(key_word) > 0:
            field = script[script.find(key_word):].replace(key_word,"")
            field = field[:field.find(",")]
            return field.replace('"','').replace(':','').replace(']','').replace('}','').strip()

    def get_product_price(self, product):
        """
        Get product price
        :param:JSON
        :return: str
        """
        path = 'price.formatted_current_price'
        return jmespath.search(path, product)


    def get_product_images(self, product):
        """
        Get product images
        :param:JSON
        :return: str
        """
        path = 'ratings_and_reviews.photos'
        photos = jmespath.search(path, product)
        if photos and photos is str:
            return photos
        elif photos and len(photos) > 0:
            product_images = []
            for product_image in photos:
                product_images.append(product_image)
            return product_images

    def get_product_description(self, product):
        """
        Get product description
        :param:JSON
        :return: str
        """
        path = 'item.product_description.downstream_description'
        return jmespath.search(path, product)

    def get_product_highlights(self, product):
        """
        Get product highlights
        :param:JSON
        :return: str
        """
        path = 'item.product_description.soft_bullets.bullets'
        bullets = jmespath.search(path, product)
        if bullets and bullets is str:
            return bullets
        elif bullets and len(bullets) > 0:
            product_highlights = []
            for product_image in bullets:
                product_highlights.append(product_image)
            return product_highlights

    def get_last_question(self, last_result):
        """
        Get last question
        :param:JSON
        :return: str
        """
        path = 'text'
        return jmespath.search(path, last_result)

    def get_last_answer_asked(self, last_result):
        """
        Get last answerasked
        :param:JSON
        :return: str
        """
        answers = jmespath.search('answers', last_result)
        if answers and len(answers) > 0:
            return jmespath.search('text', answers[0])


    def error_achive_target(self, response):
        """
        errback when scrapy.Request is fallen
        :param response:
        :return:
        """
        self.count_proxy_changing += 1
        if self.count_proxy_changing <= self.max_proxy_changing:
            self.set_proxy()
            yield scrapy.Request(self.start_urls[0], self.parse_target_page, dont_filter=True,
                                 errback=self.error_achive_target)

    def get_proxy_list(self):
        """
        Get list of proxy addresses
        :param
        :return: url
        """
        proxy_list = []
        grab = requests.get('https://free-proxy-list.net/').text
        grab = grab[grab.find('Last Checked'):]
        grab = grab.split("<tr><td>")
        for field in grab:
            if field[0].isdigit() is True:
                cur_line = field.split("</td><td>")
                if len(cur_line) > 1 and cur_line[1] == "8080":
                    cur_address = cur_line[0] + ":" + cur_line[1]
                    proxy_list.append("http://"+cur_address.strip())
        return proxy_list

    def set_proxy(self):
        """
        Set new proxy address
        :param
        :return: url
        """
        if len(self.used_proxy_addresses) == 0:
            self.used_proxy_addresses = self.get_proxy_list()
        random.shuffle(self.used_proxy_addresses)
        self.proxy = self.used_proxy_addresses[0].strip()
        del self.used_proxy_addresses[0]

    def get_response_from_xpath_list(self, xpath_string):
        """
        Get list from xpath_string
        :param xpath_string:
        :return:
        """
        return self.response.selector.xpath(xpath_string).extract()

    def get_response_from_xpath(self, xpath_string):
        """
        Get string from xpath
        :param xpath_string:
        :return:
        """
        return self.response.xpath(xpath_string).extract_first()