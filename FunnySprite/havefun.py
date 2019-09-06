import requests
import json
import pymongo

#pip3 install requests
#pip3 install pymongo

def get_answers_by_page(topic_id, page_no):
    offset = page_no * 10
    url = "https://www.zhihu.com/question/66740379/answer/272904437" # topic_url是这个话题对应的url
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    }
    r = requests.get(url, verify=False, headers=headers)
    content = r.content.decode("utf-8")
    data = json.loads(content)
    is_end = data["paging"]["is_end"]
    items = data["data"]
    client = pymongo.MongoClient()
    db = client["zhihu"]
    if len(items) > 0:
        db.answers.insert_many(items)
        db.saved_topics.insert({"topic_id": topic_id, "page_no": page_no})
    return is_end

client = pymongo.MongoClient()
db = client["zhihu"]
items = db.answers.aggregate([
    {"$match": {"target.type": "answer"}},
    {"$match": {"target.voteup_count": {"$gte": 1000}}},
    {"$addFields": {"answer_len": {"$strLenCP": "$target.content"}}},
    {"$match": {"answer_len": {"$lte": 50}}},])