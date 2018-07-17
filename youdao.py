'''
用phantomjs爬取有道翻译
有道翻译反爬进行了加密，其中
salt: 1531797921352
sign: 0adbd3c7cb2bf3370384650564ac2458
不同，先使用phantomjs爬取
'''
from selenium import webdriver
import time,datetime

key = input('输入要翻译的文字：')
print(datetime.datetime.now().strftime('%H:%M:%S'))
driver = webdriver.PhantomJS()
url = 'http://fanyi.youdao.com'
headers = {
    'Referer': 'http://fanyi.youdao.com/',
    'Cookie': 'OUTFOX_SEARCH_USER_ID=1622775053@10.168.8.61; OUTFOX_SEARCH_USER_ID_NCOO=2110065237.6420572; fanyi-ad-id=46607; fanyi-ad-closed=1; JSESSIONID=aaa7ZzN2DyC9C9W66_Lsw; ___rl__test__cookies=1531793720765',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}
driver.get(url)
# print(driver.page_source)
# driver.save_screenshot('2.png')
input = driver.find_element_by_id('inputOriginal')
input.send_keys(key)
time.sleep(3)
output = driver.find_element_by_id('transTarget')
print(output.text)
print(datetime.datetime.now().strftime('%H:%M:%S'))
# driver.save_screenshot('3.png')