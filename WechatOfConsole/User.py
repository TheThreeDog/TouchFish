# Authro     : ThreeDog
# Data       : 2019-05-28
# Function   : 将所有的用户、消息相关的操作封装在一个模块中。
# Remark     : Users中有一个字典存放所有User，User中有一个队列（list）存放所有消息

import threading
import time

import itchat
from itchat.content import *

from MyCommand import Cmd
from Common import user_type_dict,type_dict

class Msg(object):
    def __init__(self,msg,type):
        '''
        初始化消息内容，参数是从itchat接收到的msg内容。
        '''
        self.createTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msg.CreateTime)) # 创建时间
        self.text = msg.Text    # 数据内容
        self.remarkName = ''
        if msg.Type in type_dict:   # 根据数据类型做特殊处理
            self.text = type_dict[msg.Type]
        # 根据不同类型做不同判断
        if "u" == type:
            self.nickName = msg.User.NickName   # 消息发送者昵称
            self.remarkName = msg.User.RemarkName   # 消息发送者备注
            self.userName = msg.User.UserName    # 用户名，是微信接口中的id，唯一。
        elif "r" == type:
            user = Users.instance().getUserByUserName(msg.ActualUserName)
            if user is not None:
                self.remarkName = user.remarkName   # 消息发送者备注
            self.nickName = msg.ActualNickName   # 消息发送者昵称
            self.userName = msg.ActualUserName    # 用户名，是微信接口中的id，唯一。
        else :
            print("消息类型参数错误，请重试")

    def getName(self):
        if self.remarkName == '':
            return self.nickName
        return self.remarkName


class User(object):
    '''
    用户类，每个用户维护一个消息队列用于存储当前的未读消息。
    '''
    def __init__(self,*args):
        self.id =  args[0]                # id
        self.userName = args[1]           # 微信指定的的唯一用户名
        self.nickName = args[2]           # 昵称
        self.remarkName = args[3]         # 备注
        self.type = user_type_dict[args[4]] # 类型 f | r ---> 好友 | 群聊
        self.msgs = []

    def addMsg(self,msg):
        self.msgs.insert(0,msg)

    def takeMsg(self):
        return self.msgs.pop()

    def getName(self):
        if self.remarkName == "":
            return self.nickName
        return self.remarkName

    def hasNewMsg(self):        # 判断是否有新消息
        if len(self.msgs) == 0:
            return False
        else:
            return True

    def __contains__(self,e): # 重载 in / not in 运算符
        if e in self.nickName or e in self.remarkName:
            return True
        return False

    def __eq__(self,e):         # 重载 == 运算符， 如果两者用户名相同就被认为是相同的用户
        if e is None :
            return False
        return e.userName == self.userName


class Users(object):
    '''
    保存所有用户和群聊，并且提供所有的相关操作
    '''
    def __init__(self):
        self.user_count = 0
        self.selfUser = None
        self.user_dict = {}
        self.current_user = None    # 当前正在聊天的用户
        self.room_dept = -1          # 用于记录好友和群聊的分界点id
        self.cmd = Cmd(self)        # 初始化一个命令管理器， 此命令管理器管理所有的命令

        itchat.auto_login(exitCallback=itchat.logout) #登录并记录登录状态
        threading.Thread(target=itchat.run).start()             # 线程启动run实现
        self.loadUserList(itchat.get_friends(),'f')             # 加载好友
        self.loadUserList(itchat.get_chatrooms(),'r')           # 加载群聊

    @classmethod
    def instance(cls,*args,**kwargs):
        if not hasattr(Users, "_instance"):
            Users._instance = Users(*args, **kwargs)
        return Users._instance

    def exec(self):
        '''
        用户模块的事件循环
        '''
        try:
            while True:
                print(">>> ",end = '')
                cmd = input().strip() # 获取字符去除前后空格
                if cmd == '':    # 输入无效内容，直接跳过
                    continue
                if cmd == 'exit':
                    itchat.logout()
                    break
                cmd = cmd.split(' ') # 命令去除前后空格后按空格分割
                if cmd[0] not in dir(self.cmd):
                    print("命令错误，请重试")
                    continue
                # 调用cmd所匹配的函数，通过反射的形式调用  即只要用户输入指令与函数名匹配即可调用。
                getattr(self.cmd,cmd[0])(cmd[1:])

        except Exception as e:
            print(e)
            itchat.logout()

    def addUser(self,user,type):
        '''
        单独添加一个user
        '''
        new_user = User(self.user_count,user.UserName,user.NickName,user.RemarkName,type)
        self.user_dict[self.user_count] = new_user   # 键是ID，值是用户
        self.user_count += 1

    def loadUserList(self,users,type='f'):
        '''
        加载好友列表，加好友传入u，加群聊传入r
        '''
        for user in users:
            self.addUser(user,type)
        self.selfUser = self.user_dict[0]

    def hasNewMsg(self):
        '''
        判断是否有新消息，判断所有的消息列表是否为空
        '''
        for user in self.getUsers():
            if user.hasNewMsg() :  # 有新消息直接返回True
                return True
        # 均为空返回False
        return False

    def getUserByID(self,uid):
        '''
        通过ID获取用户
        '''
        if uid not in self.user_dict:
            print("用户id不存在，请重试")
            return None
        return self.user_dict[uid]

    def getUserByUserName(self,username):
        '''
        通过微信的id查找用户
        '''
        for user in self.getUsers():
            if user.userName == username:
                return user
        return None

    def getUsers(self):
        '''
        获取所有的用户
        '''
        return list(self.user_dict.values())

    def handelMsg(self,msg,type):
        '''
        处理接收到的消息，或打印或存入消息队列
        type : 好友信息是 f 群聊消息是 r
        '''
        user = self.getUserByUserName(msg.FromUserName)
        if msg['FromUserName'] == 'newsapp': # 忽略掉腾讯新闻消息
            return
        if msg['ToUserName'] == 'filehelper': # 忽略掉发给文件助手的
            return
        if msg['ToUserName'] != self.selfUser.userName: # 忽略掉发送目标不是自己的
            return
        if msg['FromUserName'] == self.selfUser.userName: # 忽略掉自己发来的消息（否则发送给群聊的消息会被排入队列）
            return
        m = Msg(msg,type)
        if user is not None:
            if user == self.current_user:  # 如果当时正在和这个人聊天 ,直接打印消息
                print("\n【{}】{} ===> ：{}\n>>> ".format(m.createTime,m.getName(),m.text),end="")
            else:                           # 如果不是的话，直接排入消息队列
                user.addMsg(m)

    def sendMsg(self,msg,username):
        itchat.send(msg,toUserName=username)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING,PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def recv_group_msg(msg):
    '''
    获取到群聊发送来的消息
    '''
    Users.instance().handelMsg(msg,'r')


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING,PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=False) # 注册消息，如果有消息收到，执行此函数。
def recv_msg(msg):
    '''
    获取到好友发送来的消息
    '''
    Users.instance().handelMsg(msg,'u')
