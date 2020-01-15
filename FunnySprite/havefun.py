# import requests
# import json
# import pymongo

# #pip3 install requests
# #pip3 install pymongo

# def get_answers_by_page(topic_id, page_no):
#     offset = page_no * 10
#     url = "https://www.zhihu.com/question/66740379/answer/272904437" # topic_url是这个话题对应的url
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
#     }
#     r = requests.get(url, verify=False, headers=headers)
#     content = r.content.decode("utf-8")
#     data = json.loads(content)
#     is_end = data["paging"]["is_end"]
#     items = data["data"]
#     client = pymongo.MongoClient()
#     db = client["zhihu"]
#     if len(items) > 0:
#         db.answers.insert_many(items)
#         db.saved_topics.insert({"topic_id": topic_id, "page_no": page_no})
#     return is_end


# get_answers_by_page()


# client = pymongo.MongoClient()
# db = client["zhihu"]
# items = db.answers.aggregate([
#     {"$match": {"target.type": "answer"}},
#     {"$match": {"target.voteup_count": {"$gte": 1000}}},
#     {"$addFields": {"answer_len": {"$strLenCP": "$target.content"}}},
#     {"$match": {"answer_len": {"$lte": 50}}},])





import os
import requests
from lxml import etree
 
# 未登录状态下，爬取知乎发现页的热门
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
}
 
session = requests.Session()
response = session.get("https://www.zhihu.com/explore", headers=headers)
print(response.text)
html = etree.HTML(response.text, etree.HTMLParser())
titles = html.xpath('//*[@id="js-explore-tab"]/div[1]/div/div/h2/a/text()')
answers = html.xpath('//*[@id="js-explore-tab"]/div[1]/div/div/div/div[4]/textarea[@class="content"]/text()')
 
print(titles)
print(answers)

print(type(titles[0])) 
# 类型是<class 'lxml.etree._ElementUnicodeResult'>
# _ElementUnicodeResult在python中是字符串的一种
# 在python3中，字符串就是指以unicode编码规则存储的数据
# 而以其他方式如utf-8，ASCII编码方式存储的数据称为bytes类型
 
# with open('zhihu.txt', 'w+', encoding='utf-8') as file:
#     for item in zip(titles, answers):
#         file.write(item[0] + item[1])
#         file.write('\n' + '*' * 50)
# print("end")