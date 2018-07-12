'''
爬取猫眼电影榜单
'''
import requests,json,time,re
from requests.exceptions import RequestException

def get_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 67.0.3396.18Safari / 537.36'
        }
        request = requests.get(url,headers=headers)
        if request.status_code ==200:
            return request.text
        return None
    except RequestException:
        return None
def parse_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern,html)
    # print(items)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }
def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_page(url)
    for item in parse_page(html):
        # print(item)
        write_to_file(item)


if __name__ == '__main__':
    offset = input('爬取到的页数：')
    for i in range(int(offset)):
        main(i*10)
