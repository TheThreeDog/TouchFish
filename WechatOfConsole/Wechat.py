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
import os
import threading
import itchat
import time
import re
from itchat.content import *

# linux常用命令，用于防止用户误输入被发送到聊天
cmd_list = ['pwd','ls','cd','grep','touch','rm','exit','bye','rm','vi',':wq',':q!',':Q!','cat','cp','mv','rmdir','mk','git','cls','clear','find']
# 构建一个字典，接收到的消息存放在此字典中，字典键是名字，值是一个列表，用于存放N条信息
msg_list = {}
# 全局int变量用于记录当前正在和谁聊天，为-1时表示不在聊天状态
current_chat_id = -1
# 好友和群聊的分界
first_room_id = 0
# 记录自己的用户名
selfUserName = ""
# 类型字典
msg_list  = {}                       # 消息列表为空
user_dict = {}
type_dict = {
    'Map':'[定位]',
    'Card':'[名片推荐]',
    'Note':'[系统消息]',
    'Sharing':'[公众号链接]',
    'Picture':'[图片]',
    'Recording':'[语音]',
    'Attachment':'[文件]',
    'Video':'[视频]'
}


# 通过用户名获取ID，后期通过ID发送消息
def getIdByUserName(name):
    for i in user_dict:
        if user_dict[i]['UserName'] == name:
            return i
    # for i in room_dict:
    #     if room_dict[i]['ChatroomName'] == name:
    #         return i
    return -1

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING,PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def recv_group_msg(msg):
    # 屏蔽腾讯新闻
    if msg['FromUserName'] == 'newsapp': # 腾讯新闻
        return
    # 过滤除了文字以外的消息
    if msg.Type in type_dict:
        msg.Text = type_dict[msg['Type']]
    chat_id = getIdByUserName(msg.FromUserName)
    if chat_id != -1:
        # print("chat_id : {} current_chat_id : {}".format(chat_id,current_chat_id))
        if chat_id == current_chat_id : # 如果这时我正在这个群里聊天
            if chat_id in user_dict:
                user_id =  getIdByUserName(msg.ActualUserName)
                username = msg.ActualNickName
                if user_id != -1:
                    username = user_dict[user_id].RemarkName
                print("\n【{}】{} ===> ：{}\n>>> ".format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msg.CreateTime)),username,msg.Text),end="")
        else: # 如果没有正在聊天，则把消息加到消息队列中  群聊消息不能直接用msg。重新封装一下
            chat_msg = {}
            chat_msg['CreateTime'] = msg.CreateTime
            chat_msg['Text'] = msg.Text
            chat_msg['NickName'] = msg.ActualNickName
            # 如果说话的这个人在自己的好友列表里，把它的名字换成备注
            user_id =  getIdByUserName(msg.ActualUserName)
            chat_msg['RemarkName'] = msg.ActualNickName
            if user_id != -1:
                chat_msg['RemarkName'] = user_dict[user_id].RemarkName
            msg_list[chat_id].insert(0,chat_msg)
    return None


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING,PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False) # 注册消息，如果有消息收到，执行此函数。
def recv_msg(msg):
    global current_chat_id
    if msg['FromUserName'] == 'newsapp': # 腾讯新闻
        return
    if msg['ToUserName'] == 'filehelper': # 发给文件助手
        print(msg)
        return
    if msg['ToUserName'] != selfUserName:
        return
    if msg['Type'] in type_dict:
        msg.Text = type_dict[msg['Type']]
    # 把消息加到消息队列当中
    chat_id = getIdByUserName(msg.FromUserName)
    if chat_id != -1:
        # print("chat_id : {} current_chat_id : {}".format(chat_id,current_chat_id))
        if int(chat_id) == int(current_chat_id) : # 如果这时我正在和这个人聊天
            if chat_id in user_dict:
                username = user_dict[chat_id]['RemarkName']
                if username == '':
                    username = user_dict[chat_id]['NickName']
                print("\n【{}】{} ===> ：{}\n>>> ".format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msg.CreateTime)),username,msg.Text),end="")
        else:                           # 如果没有正在聊天，则把消息加到消息队列中
            msg_list[chat_id].insert(0,msg)
    return None

def ls(arg):
    '''
    获取最新消息列表
    '''
    # print(arg)
    if len(arg) == 0:         # ls 没有参数：获取所有消息列表
        # print("msgList : " ,msg_list)
        max_count = max(len(x) for x in msg_list.values())
        if max_count == 0:
            print("消息列表为空")
        else:
            for i in msg_list:
                if len(msg_list[i]) != 0 :  # 消息列表必须不为空
                    # 个人消息
                    if i in user_dict:
                        name = user_dict[i]['RemarkName']
                        if name == '':
                            name = user_dict[i]['NickName']
                        print("【id:{:^3} 】 {:^10} 发来 {:^3} 条未读消息".format(i,name,len(msg_list[i])))
                    # 群聊消息
                    # elif i in room_dict:
                    #     name = room_dict[i]['NichName']
                    #     print(" {:^4} 发来 {:^3} 条未读消息【id:{} 】".format(name,len(msg_list[i]),i))

    elif arg[0] == '-f':    # ls -f 好友列表
        print("好友列表：")
        for user_index in user_dict:
            name = user_dict[user_index]['RemarkName']
            if name == '':
                name = user_dict[user_index]['NickName']
            if user_index >= first_room_id:# 说明是群聊
                print(" {:^4}：【群聊】{:^3} ".format(user_index,name))
            else:
                print(" {:^4}：{:^3} ".format(user_index,name))

    # elif arg[0] == '-r':    # ls -r 群聊列表
    #     for room_index in room_dict:
    #         name = room_dict[room_index]['NickName']
    #         print(" {:^4}：{:^3} ".format(room_index,name))
    else :
        print('参数错误，请重试')

def cd(arg):
    global current_chat_id
    if len(arg) == 0 :
        print("cd命令需要参数")
        return
    elif arg[0] == '..':
        # 返回主页
        return
    else:
        try:
            c_id = int(arg[0])
            current_chat_id = c_id
            user = user_dict[current_chat_id]
            cls(None)
            # 进来后，先把队列当中的消息显示出来
            while len(msg_list[c_id]) != 0:
                msg = msg_list[c_id].pop()
                # 如果是群聊，username从msg中获取
                if current_chat_id >= first_room_id:
                    username = msg['NickName']
                else:
                    username = user['RemarkName']
                    if username == '':
                        username = user['NickName']
                print("【{}】{} ===> ：{}".format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msg['CreateTime'])),username,msg['Text']))

            while True:
                name = user.RemarkName
                if name == '':
                    name = user.NickName
                print(" 与 {} 聊天中 >>> ".format(name),end = '')
                msg = input()
                if msg == 'cd ..':
                    # 退出聊天，把当前聊天的id置为-1
                    current_chat_id = -1
                    break
                # 如果输入内容包含疑似cmd字符串，这个len不为0
                if len(list(filter(lambda x:True if x in msg else False,cmd_list))) > 0:
                    print("您的输入中包含疑似shell终端命令的字符串，确认发送此消息吗？y or n")
                    res = input()
                    if res == 'y' or res == '\n':
                        pass
                    else:
                        continue
                # 如果能走到这一步就发送数据
                itchat.send(msg,toUserName=user.UserName) # 将信息发送给user

        except Exception as e:
            print(e)
            print('参数错误，请重试')
            return


def find(arg):
    '''
    通过字符串查找对象
    '''
    print(arg)
    if len(arg) == 0:
        print("参数错误，请重试")
        return

    print("查找到以下好友|群聊：")
    for i in user_dict:
        if arg[0] in user_dict[i]['RemarkName'] or arg[0] in user_dict[i]['NickName']:
            if i >= first_room_id:# 说明是群聊
                print(" {:^4}：【群聊】{:^4}  {:^4} ".format(i,user_dict[i]['RemarkName'],user_dict[i]['NickName']))
            else:
                print(" {:^4}：{:^4}  {:^4} ".format(i,user_dict[i]['RemarkName'],user_dict[i]['NickName']))

    # print("查找到以下群聊：")
    # for i in room_dict:
    #     if arg[0] in room_dict[i]['NickName']:
    #         print(" {:^4}：{:^4} ".format(i,room_dict[i]['NickName']))


def cls(arg): #清屏
    print("\033c",end='')


# 回调：命令与处理函数绑定，方便后期动态扩展
callBack = {
    'ls':ls,
    'find':find,
    'cd':cd,
    'cls':cls,
}

# 主程序
if __name__ == '__main__':
    try:
        itchat.auto_login(hotReload=True,enableCmdQR = 2,exitCallback=itchat.logout) #登录并记录登录状态
        threading.Thread(target=itchat.run).start()             # 线程启动run实现
        user_list = itchat.get_friends()    # 获取好友
        selfUserName = user_list[0]['UserName']
        room_list = itchat.get_chatrooms()  # 获取群聊
        # room_dict = {}
        chat_id = 0
        for user in user_list:
            user_dict[chat_id] = user       # id 和昵称存储用户信息
            msg_list[chat_id] = []
            chat_id += 1
        for room in room_list:
            if first_room_id == 0:
                first_room_id = chat_id
            user_dict[chat_id] = room
            msg_list[chat_id] = []
            chat_id += 1

        while True:
            print(">>> ",end = '')
            cmd = input().strip() # 获取字符去除前后空格
            if cmd == '':    # 输入无效内容，直接跳过
                continue
            if cmd == 'exit':
                itchat.logout()
                break
            cmd = cmd.split(' ') # 命令去除前后空格后按空格分割
            if cmd[0] not in callBack:
                print("命令错误，请重试")
                continue
            callBack[cmd[0]](cmd[1:]) # 调用cmd所匹配的函数
    except Exception as e:
        print(e)
        itchat.logout()




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
