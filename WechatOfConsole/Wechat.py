# Authro     : ThreeDog
# Data       : 2019-04-29
# Thanks     : 底层使用itchat ：https://github.com/littlecodersh/itchat
# Function   : 在控制台使用微信，通过接口调用，接收并发送消息。 接收端需要一个线程来itchat.run()执行。
# Remark     : 仅支持文字消息，尽可能保持微信的用户体验
    # 'ls': 显示所有未读消息,
    # 'ls -f':显示所有的好友|群聊列表,
    # 'find XXX':通过姓名查找模糊查找好友或群聊,
    # 'cd {id}':进入与id为{id}的用户或群聊聊天,
    # 'cd ..':退出当前聊天返回上一级,
    # 'cls'：清空屏幕
    # 'exit'：退出程序,,
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

from User import Users

# 主程序
if __name__ == '__main__':
    users = Users.instance()            # 初始化好友列表 (单例模式)
    users.exec()                        # 进入users的事件循环    



'''

itchat.send("Hello World!"，toUserName=None) # 讲信息发送给user
ithcat.send("@fil@%s" % '/tmp/test.text')
ithcat.send("@img@%s" % '/tmp/test.png')
ithcat.send("@vid@%s" % '/tmp/test.mkv')

@itchat.msg_register(TEXT)   #这里的TEXT表示如果有人发送文本消息，那么就会调用下面的方法
def simple_reply(msg):
    #这个是向发送者发送消息
    itchat.send_msg('已经收到了文本消息，消息内容为%s'%msg['Text'],toUserName=msg['FromUserName'])
    return "T reveived: %s" % msg["Text"]     #返回的给对方的消息，msg["Text"]表示消息的内容

itchat.get_friends()  返回完整的好友列表、
每个好友为一个字典, 其中第一项为本人的账号信息;
传入 update=True, 将更新好友列表并返回, get_friends(update=True)

# 获取任何一项等于name键值的用户
itchat.search_friends(name='autolife')
获取备注,微信号, 昵称中的任何一项等于name键值的用户. (可以与下一项配置使用.)

get_mps
将返回完整的工作号列表
每个公众号为一个字典,
传入 update=True 将更新公众号列表, 并返回.

get_chatrooms : 返回完整的群聊列表.
search_chatrooms : 群聊搜索.
update_chatroom : 获取群聊用户列表或更新该群聊.
memberList = itchat.update_chatroom('@@abcdefg1234567', detailedMember=True)

msg:
{'VoiceLength': 0, 'MsgType': 1, 'Type': 'Text', 'FromUserName': '@92f11606bce53a6363bef288374179e2ab88a1ef045fa56252ab3dbee23b4a18', 'NewMsgId': 8717003480232085925, 'Url': '', 'StatusNotifyUserName': '', 'MediaId': '', 'FileSize': '', 'Content': '发什么', 'Ticket': '', 'Text': '发什么', 'ToUserName': '@61ed504db10ac7cf1ba777384ef94cf8d3134486e1ccbfac853e6c1bf7cab5a8', 'ImgWidth': 0, 'MsgId': '8717003480232085925', 'Status': 3, 'EncryFileName': '', 'ImgStatus': 1, 'StatusNotifyCode': 0, 'AppInfo': {'AppID': '', 'Type': 0}, 'PlayLength': 0, 'HasProductId': 0, 'RecommendInfo': {'VerifyFlag': 0, 'OpCode': 0, 'NickName': '', 'Ticket': '', 'UserName': '', 'Content': '', 'Scene': 0, 'AttrStatus': 0, 'Alias': '', 'Sex': 0, 'Province': '', 'Signature': '', 'QQNum': 0, 'City': ''}, 'OriContent': '', 'ImgHeight': 0, 'User': <User: {'Uin': 0, 'Statues': 0, 'UserName': '@92f11606bce53a6363bef288374179e2ab88a1ef045fa56252ab3dbee23b4a18', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=685068817&username=@92f11606bce53a6363bef288374179e2ab88a1ef045fa56252ab3dbee23b4a18&skey=@crypt_126596ce_c3c7d1f500bed8cb9c2e2190c2188bba', 'MemberList': <ContactList: []>, 'KeyWord': '', 'PYQuanPin': '54F3yiciguoxiaofendui2hao', 'MemberCount': 0, 'AppAccountFlag': 0, 'ChatRoomId': 0, 'IsOwner': 0, 'AttrStatus': 102501, 'Sex': 2, 'ContactFlag': 3, 'RemarkPYQuanPin': 'zeze', 'PYInitial': '54F3YCGXFD2H', 'NickName': '5.4F3一次过小分队2号', 'EncryChatRoomId': '', 'SnsFlag': 1, 'HideInputBarFlag': 0, 'DisplayName': '', 'VerifyFlag': 0, 'StarFriend': 0, 'RemarkPYInitial': 'ZZ', 'Province': '山西', 'RemarkName': '泽泽', 'Alias': '', 'Signature': '', 'UniFriend': 0, 'City': '临汾', 'OwnerUin': 0}>, 'ForwardFlag': 0, 'CreateTime': 1557062982, 'SubMsgType': 0, 'AppMsgType': 0, 'FileName': ''}



'''
