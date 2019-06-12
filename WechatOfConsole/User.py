# Authro     : ThreeDog
# Data       : 2019-05-28
# Function   : 将所有的用户、消息相关的操作封装在一个模块中。
# Remark     : Users中有一个字典存放所有User，User中有一个队列（list）存放所有消息

from MyCommand import Cmd
from Common import user_type_dict

class Msg(object):
    def __init__(self,msg):
        '''
        初始化消息内容，参数是从itchat接收到的msg内容。
        '''
        self.createTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msg.CreateTime)) # 创建时间
        self.text = msg.Text    # 数据内容
        if msg.Type in type_dict:   # 根据数据类型做特殊处理
            self.text = type_dict[msg.Type]
        self.nickName = msg.User.NickName   # 消息发送者昵称
        self.remarkName = msg.User.RemarkName   # 消息发送者备注
        self.userName = msg.UserName    # 用户名，是微信接口中的id，唯一。

    def getName(self):
        if self.remarkName == '':
            return self.nickName
        return self.remarkName


class User(object):
    '''
    用户类，每个用户维护一个消息队列用于存储当前的未读消息。
    '''
    def __init__(self，*args):
        self.id =  args[0]                # id
        self.userName = args[1]           # 微信指定的的唯一用户名
        self.nickName = args[2]           # 昵称
        self.remarkName = args[3]         # 备注
        self.type = user_type_dict[args[4]] # 类型 u | r ---> 好友 | 群聊
        self.msgs = []
    
    def getName(self):
        if self.remarkName == "":
            return self.nickName
        return self.remarkName
    
    def hasNewMsg():        # 判断是否有新消息
        if len(self.msgs) == 0:
            return False
        else:
            return True
    
    def __contains__(self,e): # 重载 in / not in 运算符
        if e in self.nickName or e in self.remarkName:
            return True
        return False
    

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

    def addUser(self,user,type):
        '''
        单独添加一个user
        '''
        new_user = User(user_count,user.UserName,user.NickName,user.RemarkName,type)
        self.user_dict[user_count] = new_user   # 键是ID，值是用户
        user_count += 1

    def loadUserList(self,users,type='u'):
        '''
        加载好友列表，加好友传入u，加群聊传入r
        '''
        for user in users:
            self.addUser(user,type)
        self.selfUser = self.user_dict[0]

    def recvMsg(self,msg):
        '''
        接收到消息，归类排入消息队列
        '''
        m = Msg(msg)
        # 如果当前正在和他聊天
        if current_user.userName == m.userName:
            # 直接将消息打印
            print("\n【{}】{} ===> ：{}\n>>> ".format(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(m.createTime)),m.userName,m.text),end="")
            return 

        for user in self.getUsers():
            if user.userName == msg.userName:
                user.msg_list.insert(0,m)       # 将消息存入队列当中
                # msg_list[chat_id].insert(0,chat_msg)

    def hasNewMsg(self):
        '''
        判断是否有新消息，判断所有的消息列表是否为空
        '''
        for user in self.getUsers():
            if user.hasNewMsg() :  # 有新消息直接返回True
                return True
        # 均为空返回False
        return False
    
    def getUser(uid):
        '''
        通过ID获取用户
        '''
        if uid not in self.user_dict:
            print("用户id不存在，请重试")
        return self.user_dict[uid]


    def getUsers(self):
        '''
        获取所有的用户
        '''
        return list(self.user_dict.values())

