from selenium import webdriver

# 要想调用键盘按键操作需要引入keys包
from selenium.webdriver.common.keys import Keys

driver = webdriver.PhantomJS()
driver.get("http://www.baidu.com/")
data = driver.find_element_by_id("wrapper").text
# print(data)
# print(driver.title)
# print(driver.page_source) 
# driver.save_screenshot('baidu.png')
# print(driver.get_cookies())
# driver.find_element_by_id("kw").send_keys(Keys.CONTROL,'a')
# driver.quit()
print(driver.current_url)