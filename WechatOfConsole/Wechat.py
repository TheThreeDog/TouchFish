# Authro     : ThreeDog
# Data       : 2019-04-29
# Thanks     : 底层使用itchat ：https://github.com/littlecodersh/itchat
# Function   : 在控制台使用微信，通过接口调用，接收并发送消息。 接收端需要一个线程来itchat.run()执行。
# Remark     : 仅支持文字消息，尽可能保持微信的用户体验
# Requests   : 
    #   - pip install itchat
    # 7、仅支持单行输入，一旦换行会有显示上的bug
import platform

if platform.system().lower() != 'linux':
    print("不支持的平台：{}".format(platform.system().lower()))
    exit(0)

import User
import sys
from translator import translator

# 主程序
if __name__ == '__main__':
    with open(".errorlog","a+") as f:           # 从定向错误输出
        sys.stderr = f     
    translator.load("lang/en_US.ts")            # 翻译机、默认加载中文
    users = User.Users.instance()               # 初始化好友列表 (单例模式)
    users.exec()                                # 进入users的事件循环
