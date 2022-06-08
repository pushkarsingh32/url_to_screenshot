import logging

import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess
from PIL import Image as pil_image
from io import BytesIO
import re


logging.getLogger('scrapy').setLevel(logging.WARNING)


# logging.getLogger('scrapy').propagate = False


def get_post_url_list(path):
    # Getting URLs list from csv file
    print(f"url file path is {path}")
    df = pd.read_csv(path, encoding='utf8')
    print(df)
    post_url_lists = df['URL'].tolist()
    post_url_lists = list(set(post_url_lists))
    for urls in post_url_lists:
        if urls == 'nan':
            post_url_lists.remove(urls)

    print(f"{post_url_lists}")
    return post_url_lists


def convert_to_dict(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


class ScreenShotSpider(scrapy.Spider):
    name = 'screenshot'
    screenshot_api_url = "https://cdn.statically.io/screenshot/:"

    def parse(self, response):
        full_webpage_url = response.url
        webpage_url = re.sub('https://', '', full_webpage_url)

        request_url = self.screenshot_api_url + webpage_url
        yield scrapy.Request(url=request_url, callback=self.parse_screenshot_response,
                             meta={'web_address': response.url})

    def parse_screenshot_response(self, response):
        print(response.url)
        img = pil_image.open(BytesIO(response.content))
        img.show()
        full_image_name = self.path + response.meta['web_address'] + ".jpg"
        img.save(full_image_name)


#
#     ext = tldextract.extract(response.url)
#     # get_domain_name = ext.domain
#     # domain_name = '.'.join(part for part in ext if part)
#     # This will find all the internal links from the given url
#     internal_links = LxmlLinkExtractor(allow_domains=ext.registered_domain, unique=True,
#                                        deny=('category', 'page', 'author', 'tos', 'privacy',
#                                              'contact', 'about', 'advertise', 'write-for-us',
#                                              'tag')
#                                        ).extract_links(response)
#
#     internal_links = [str(link.url) for link in internal_links]
#     for link in internal_links:
#         yield scrapy.Request(url=link,
#                              callback=self.parse_internal_link,
#                              meta={'domain_name': response.url})
#
#
# def parse_internal_link(self, response):
#     ext = tldextract.extract(response.url)
#     get_domain_name = ext.registered_domain
#     if get_domain_name in self.reject:
#         print("It is 1")
#     restrict_words = [get_domain_name]
#     for word in self.reject:
#         restrict_words.append(word)
#     restrict_words_tuple = tuple(restrict_words)
#     external_links = LxmlLinkExtractor(allow_domains=(),
#                                        unique=True,
#                                        deny=restrict_words_tuple,
#                                        ).extract_links(response)
#     external_links = [str(link.url) for link in external_links]
#
#     for external_link in external_links:
#         for word in self.reject:
#             if word in str(external_link):
#                 # print(f'1 bad word {word} in {external_link}')
#                 break
#         yield scrapy.Request(url=external_link, callback=self.parse_external_link,
#                              meta={'on_post': response.url,
#                                    'from_domain': response.meta['domain_name']})
#
#
# def parse_external_link(self, response):
#     # Checking Each Internal links for bad words before saving into database
#
#     for word in self.reject:
#         if word in str(response.url):
#             # print(f'2 bad word {word} in {response.url}')
#             return
#     # This is for finding Registered Domain of external link
#     ext2 = tldextract.extract(response.url)
#     print(f'External URL: {response.url}')
#     dic = {'external_website': ext2.registered_domain, 'external_link': response.url,
#            'on_post': response.meta['on_post'],
#            'from_domain': response.meta['from_domain']}
#     df = pd.DataFrame(dic, index=[0])
#     df.to_csv(self.path, mode='a', header=False)
#     df = pd.read_csv(self.path, index_col=0)
#     df.drop_duplicates(subset='external_website', keep='first', inplace=True)
#     df = df.dropna()
#     df = df.reset_index(drop=True)
#     df.to_csv(self.path, mode='w', header=True)


def ask_user(question):
    response = input(question + ' y/n' + '\n')
    if response == 'y':
        return True
    else:
        return False


def create_file(path):
    response = False
    # if os.path.exists(path):
    #     response = ask_user('File already exists, replace?')
    #     if not response:
    #         return

    with open(path, 'wb') as file:
        file.close()


def scrapy_process_create(url_file_path, extracting_screenshot_data, reject=[]):
    #
    print('Collecting Web Post URLs...')
    # post_urls = get_post_url_list(url_file_path)
    post_urls = ['https://cookeryspace.com/cook-eggs-on-induction/',
                 'https://cookeryspace.com/will-granite-rock-pan-work-on-an-induction-cooktop/']

    print('Extracting Headings...')
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    process = CrawlerProcess({'USER_AGENT': USER_AGENT})
    process.crawl(ScreenShotSpider, start_urls=post_urls, path=extracting_screenshot_data,
                  reject=reject)
    process.start()


def call_main_function():
    bad_words = []
    url_file_path = './data/urls'
    extracting_screenshot_data = './data/screenshots'
    scrapy_process_create(url_file_path, extracting_screenshot_data, reject=bad_words)
    # print(f"from main function\n{df.head()}")


if __name__ == '__main__':
    call_main_function()
