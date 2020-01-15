
from bs4 import BeautifulSoup
import requests
import random
import time
import sys
import threading

THREAD_COUNT=100

# 57694260   57694280
def get_titles(start,end):
    print("开始爬取标题：{} ～ {}".format(start,end))
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    proxies=[]
    with open("ProxyPoolByMe/proxies.txt") as proxy_file:
        for proxy in proxy_file.readlines():
            proxies.append({"http":"http://{}".format(proxy.replace("\n","")),"https":"https://{}".format(proxy.replace("\n",""))})
    proxy = random.choice(proxies)
    question_file = open("questions.txt","a+")
    file_404 = open("404.txt","a+")

    # for 循环无法控制出错的id回轮，用while手动控制逻辑
    i = int(start)
    end = int(end)
    # end = end
    while i < end:
        try:
            res = requests.get("https://www.zhihu.com/question/{}".format(i),headers=headers,timeout=(5,5))
            title = BeautifulSoup(res.content,'lxml').title.string
            if "安全验证" in title:
                print("{} 触发了安全验证".format(proxy))
                proxy = random.choice(proxies)
                print("更换代理为：{}".format(proxy))
                continue
            elif "404" in title:  # 404
                print("404:",i)
                file_404.write(str(i)+"\n")
            else:
                print(str(i)+"    "+title)
                question_file.write(str(i)+"    "+title+"\n")
            i += 1
            time.sleep(random.random()*4+1)

        except Exception as e: # 如果代理不可用
            print("代理错误")
            proxy = random.choice(proxies)



# python3.6 zhihu.py 57694200 57694300
if __name__ == "__main__":
    get_titles(57694300,57694400)
    # s = int(sys.argv[1])
    # e = int(sys.argv[2])
    # step = (e-s)/THREAD_COUNT

    # threads = []
    # while s<e :
    #     # 启动多线程爬取不同段的ID
    #     t = threading.Thread(target=get_titles,args=(s,s+step))
    #     s = s+step 
    #     threads.append(t)
    #     t.start()

    # # 等待所有线程任务结束。
    # for t in threads:
    #     t.join()