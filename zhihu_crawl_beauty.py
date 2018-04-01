from random import choice
from my_agent import CUSTOM_USER_AGENT
import requests
from Queue import Queue
from lxml import etree
import time
from ParseImage import ParseImage
from threading import Thread

url_queue = Queue()
content_queue = Queue()

topic_id = '30502941'
BASE_URL = 'https://www.zhihu.com/api/v4/questions/%s/answers'% topic_id
REFER_URL = 'https://www.zhihu.com/question/%s'% topic_id
BASE_QUERY = '''?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&offset=0&sort_by=default'''
AUTHORITY_HEAD = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'


def parse_url(url):
    agent = choice(CUSTOM_USER_AGENT)
    headers={'User-Agent': agent, 'refer':REFER_URL, 'authorization':AUTHORITY_HEAD}
    try:
        resp = requests.get(url=url, headers=headers)
        print url
        return resp.json()
    except Exception as e:
        return None


def parse_result(item):
    is_end = is_result_empty(item)
    if is_end is True:
        return
    if 'data' in item and len(item['data'])>0:
        data_list = item['data']
        for image_content in data_list:
            url_queue.put({"data":image_content})
    if not item["paging"]["is_end"]:
        url_queue.put({"url":item["paging"]['next']})


def parse_answer(content):
    user_agent = choice(CUSTOM_USER_AGENT)
    image_content = content['content']
    html_str = etree.HTML(image_content)
    path = "//img//@src"
    author_name = content["author"]["name"]
    images = html_str.xpath(path)
    for image in images:
        if not image.startswith("http"):
            continue
        image = ParseImage(img_src=image, author_name=author_name, user_agent=user_agent)
        image.save_image()


def is_result_empty(item):
    if item is None:
        return True
    if item['data'] is None:
        return True
    if len(item['data']) == 0:
        return True
    next_page = item['paging']
    if next_page['is_end'] is True:
        return True
    return False


def init():
    url = BASE_URL + BASE_QUERY
    answer = parse_url(url)
    parse_result(answer)
    time.sleep(5)


def produce_item(url):
    item_content = parse_url(url)
    if item_content is None:
        return
    parse_result(item_content)
    time.sleep(2)


def consume_item(content):
    parse_answer(content)
    time.sleep(5)


if __name__ == '__main__':
    init()
    while url_queue.not_empty:
        queue_item = url_queue.get()
        if 'data' in queue_item:
            t = Thread(target=consume_item, args=(queue_item['data'],))
            t.start()
        if 'url' in queue_item:
            url = queue_item['url']
            t = Thread(target=produce_item, args=(url,))
            t.start()