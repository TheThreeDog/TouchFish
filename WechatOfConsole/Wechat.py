# Authro     : ThreeDog
# Data       : 2019-04-29
# Thanks     : 底层使用itchat ：https://github.com/littlecodersh/itchat
# Function   : 在控制台使用微信，通过接口调用，接收并发送消息。 接收端需要一个线程来itchat.run()执行。
# Remark     : 仅支持文字消息，尽可能保持微信的用户体验
# Requests   : 
    #   - pip install itchat
    #   - pip install pygame
# Requests：
    # 待开发需求：
    # １、中文删除存在BUG
    # ２、上下左右光标不能移动
    # 3、文字编辑过程中，新来的消息会干扰输入
    # 4、添加设置模块
    #   1、设置中英文切换
    #   2、用文件保存设置
    #   3、
    # 5、新开发自动回复功能
    # 6、群发助手
    # 7、仅支持单行输入，一旦换行会有显示上的bug

import User
from translator import translator

# 主程序
if __name__ == '__main__':
    translator.load("lang/zh_CN.ts")            # 翻译机、默认加载中文
    users = User.Users.instance()               # 初始化好友列表 (单例模式)
    users.exec()                                # 进入users的事件循环
