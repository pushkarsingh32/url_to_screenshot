import json
import base64
import scrapy
from scrapy_splash import SplashRequest


class ExtractSpider(scrapy.Spider):
    name = 'extract'

    def start_requests(self):
        url = 'https://stackoverflow.com/'
        splash_args = {
            'html': 1,
            'png': 1
        }
        yield SplashRequest(url, self.parse_result, endpoint='render.json', args=splash_args)

    def parse_result(self, response):
        imgdata = base64.b64decode(response.data['png'])
        filename = 'some_image.png'
        with open(filename, 'wb') as f:
            f.write(imgdata)


    # def parse_result(self, response):
    #     png_bytes = base64.b64decode(response.data['png'])
    #
    #     imgdata = base64.b64decode(png_bytes)
    #     filename = 'some_image.png'
    #     with open(filename, 'wb') as f:
    #         f.write(imgdata)

