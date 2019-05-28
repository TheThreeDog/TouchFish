# Authro     : ThreeDog
# Data       : 2019-05-28
# Function   : 将所有的用户、消息相关的操作封装在一个模块中。
# Remark     : UserDict中有一个字典存放所有User，User中有一个队列（list）存放所有消息

chat_msg['Text'] = msg.Text
chat_msg['NickName'] = msg.User.NickName
chat_msg['RemarkName'] = msg.User.RemarkName

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

class Msg(object):
    def __init__(self,msg):
        '''
        初始化消息内容，参数是从itchat接收到的msg内容。
        '''
        self.createTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(msg.CreateTime) # 创建时间
        self.text = msg.Text    # 数据内容
        if msg.Type in type_dict:   # 根据数据类型做特殊处理
            self.text = type_dict[msg.Type]
        self.nickName = msg.User.NickName   # 消息发送者昵称
        self.remarkName = msg.User.RemarkName   # 消息发送者备注
        self.userName = msg.UserName    # 用户名，是微信接口中的id，唯一。
        self.ActualUserName = msg.ActualUserName # 群聊当中

    def getName(self):
        if self.remarkName == '':
            return self.nickName
        return


class User(object):
    '''
    用户类，每个用户维护一个消息队列用于存储当前的未读消息。
    '''
    def __init__(self):
        self.id = None
        self.nickName = None
        self.remarkName=None
        self.msgs = []


class UserDict(object):
    def __init__(self):
        self.user_dict = {}
        self.current_user = None # 当前正在聊天的用户

    def loadUserList(self,users):
        '''
        加载好友列表
        '''
        pass

    def recvMsg(self,msg):
        '''
        接收到消息，归类排入消息队列

        '''
        pass
