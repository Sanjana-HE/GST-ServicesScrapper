import scrapy
import csv
import json
from gstServices.items import GstservicesItem


class QuotesSpider(scrapy.Spider):
    # name of crawler
    name = "services"
    # url of site to be crawled
    start_urls = ['https://www.indiafilings.com/find-gst-rate']

    # parse each of titles obtained
    # make request to each of the titles to get corresponding data
    def parse(self, response):
        titles = response.xpath('//*[@id="Services33"]/div/div/div')
        i = 1
        for title in titles:
            yield scrapy.FormRequest(url="https://www.indiafilings.com/services.php",
                                     formdata={'attribute': title.xpath('h5/@data-service').extract()[0]},
                                     callback=self.parse_title_page, dont_filter=True, meta={'title': title.xpath(
                    'h5/text()').extract()[0], 'id': i})
            i = i + 1

    # parse each of data in each titles
    def parse_title_page(self, response):
        title = response.meta["title"]
        try:
            table_rows = response.xpath('/html/body/div[@class="table-responsive"]/table/tbody')
            row = table_rows.xpath('tr')[0]
            sub_title = ''
            description = ''
            sac_code = ''

            # looping through each of rows obtained to seperate title, sub_title,description
            for row in table_rows.xpath('tr'):
                temp_sub_title = row.xpath('td/strong/text()').extract()
                if len(temp_sub_title) > 0:
                    sub_title = temp_sub_title[0]
                    description = ''
                    sac_code = ''
                    continue
                _description = row.xpath('td[1]/text()').extract()
                if len(_description) > 0:
                    description = _description[0]
                _sac_code = row.xpath('td[2]/text()').extract()
                if len(_sac_code) > 0:
                    sac_code = _sac_code[0]
                if sac_code != '':
                    try:
                        # making request to find gst rate for each view button
                        re = scrapy.FormRequest(url="https://www.indiafilings.com/get-description.php",
                                                formdata={'query': description, 'section': 'Services'},
                                                callback=self.parse_rate, dont_filter=True, meta={'title': title,
                                                                                                  'sub_title': sub_title,
                                                                                                  'description': description,
                                                                                                  'sac_code': sac_code,
                                                                                                  'id': response.meta[
                                                                                                      'id']})
                    except Exception as e:
                        print "Exception: e", e
                        print "sub title is " + sub_title
                        print "description is  " + description
                        print "sac code is " + sac_code
                    else:
                        yield re



        except Exception as e:
            print "not valid", e

    # function to get gst rates and yield it to csv file
    def parse_rate(self, response):
        if response.body:
            rateArr = json.loads(response.body)
            rate = rateArr[0]['rate']
            title = response.meta["title"],
            sub_title = response.meta["sub_title"],
            description = response.meta["description"],
            sac_code = response.meta["sac_code"]

            yield GstservicesItem(title=title, sub_title=sub_title, description=description, sac_code=sac_code,
                                  rate=rate, id=response.meta['id'])
        else:
            print "iiiiiinnnnnn ellllssseeee"
            title = response.meta["title"],
            sub_title = response.meta["sub_title"],
            description = response.meta["description"],
            sac_code = response.meta["sac_code"]
            yield GstservicesItem(title=title, sub_title=sub_title, description=description, sac_code=sac_code,
                                  id=response.meta['id'])