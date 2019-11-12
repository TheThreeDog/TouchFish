from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import os 
import sys

question_file = open("questions.txt","w+")
file_404 = open("404.txt","w+")

os.environ["webdriver.chrome.driver"] = "/home/threedog/ThreeDog/Some-Commen-Code/知乎爬虫/chromedriver"

# req_url = "https://www.zhihu.com/question/30964702"
req_url = "https://www.zhihu.com/question/"
chrome_options=Options()

proxys = []
with open("ProxyPoolByMe/proxies.txt") as proxy_file:
	for proxy in proxy_file.readlines():
		proxys.append(proxy.replace("\n",""))
proxy = random.choice(proxys)
# '114.249.230.208:8000'
chrome_options.add_argument('--headless')
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument('--proxy-server=http://'+proxy)

# 设置chrome浏览器无界面模式

# 无界面服务器上使用。

browser = webdriver.Chrome("/home/threedog/ThreeDog/Some-Commen-Code/知乎爬虫/chromedriver",chrome_options=chrome_options)
# browser = webdriver.Chrome()
# 开始请求
# browser.get(req_url)
#打印页面源代码
# print(browser.page_source)
#//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/span
# //*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div[6]/div/div[2]/div[1]/span

for i in range(57694260,57694280):
	url = req_url+str(i)
	browser.get(url)
	print(browser.title)
	if "安全验证" in browser.title: # 更换代理:
		print("出现安全验证:",proxy)
		print(chrome_options._arguments)

	browser.close()
	chrome_options._arguments.clear()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument("--no-sandbox")
	proxy = random.choice(proxys)
	chrome_options.add_argument('--proxy-server=http://'+proxy)
	browser = webdriver.Chrome("/home/threedog/ThreeDog/Some-Commen-Code/知乎爬虫/chromedriver",chrome_options=chrome_options)

	if "404" not in browser.title:  # 404
		print("error:",i)
		file_404.write(str(i)+"\n")
	else:
		print(i)
		question_file.write(str(i)+"\n")
	# time.sleep(random.choice(range(5)))
'''
for i in range(1,150):
	try:
		text = browser.find_element_by_xpath('//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div['+str(i)+']/div/div[2]/div[1]/span').text
		print('【'+str(i)+'】')
		print(text)

	except Exception as e:
		print(e)
	browser.execute_script('window.scrollBy(0,1200)')
	time.sleep(random.choice(range(5)))
'''
question_file.close()
file_404.close()
#关闭浏览器
browser.close()
#关闭chreomedriver进程
browser.quit()