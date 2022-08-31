from multiprocessing.sharedctypes import Value
from urllib import response
import requests
import lxml.html as html
import os
import datetime

HOME_URL='https://www.lahora.com.ec/'
XPATH_LINK_TO_ARTICLE= '//div[@class="main-story" or @class="side-story"]/h3/a/@href'
XPATH_TITLE='//h1[@class="entry-title"]/text()'
XPATH_SUB_TITLE='//div[@class="entry-content"]/p/em/strong/text()'
XPATH_BODY='//div[@class="entry-content"]/p[not(@class)] /text()'


def parse_notice(link,today):
    try:
        response=requests.get(link)
        if response.status_code==200:
            notice=response.content.decode('utf-8')
            parsed=html.fromstring(notice)
            try:
                title=parsed.xpath(XPATH_TITLE)[0]
                title=title.replace('\"', ' ')
                sub_title=parsed.xpath(XPATH_SUB_TITLE)[0]
                body=parsed.xpath(XPATH_BODY)
            except IndexError:
                return

            with open(f'{today}/{title}.txt','w',encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(sub_title)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response=requests.get(HOME_URL)
        if response.status_code == 200:
            Home=response.content.decode('utf-8')
            parsed=html.fromstring(Home)
            links_to_notice=parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notice)
            today=datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notice:
                parse_notice(link,today)
        else:
            raise ValueError(f'Error{response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()

if __name__ == '__main__':
    run()