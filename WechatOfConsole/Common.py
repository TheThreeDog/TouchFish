# Authro     : ThreeDog
# Data       : 2019-06-12
# Function   : 共同包，存放一些公共的定义，主要是程序中用到文字转化的地方

from tdinput import td_input
from translator import tdtr

# 消息类型，转化成对应的消息类型显示
type_dict = {
    'Map':tdtr('[定位]'),
    'Card':tdtr('[名片推荐]'),
    'Note':tdtr('[系统消息]'),
    'Sharing':tdtr('[公众号链接]'),
    'Picture':tdtr('[图片]'),
    'Recording':tdtr('[语音]'),
    'Attachment':tdtr('[文件]'),
    'Video':tdtr('[视频]')
}

# linux常用命令列表，用于防止用户误输入被发送到聊天
cmd_list = ['pwd','ls','cd','grep','touch','rm','exit','bye','rm','vi',':wq',':q!',':Q!','cat','cp','mv','rmdir','mk','git','cls','clear','find']

# 群聊还是个人
user_type_dict = {
    'r':tdtr('【群聊】'),
    'f':tdtr('【好友】'),
}

class History(object):
    '''
    输入历史，所有的输入历史都保存在这里。 类似一个队列 
    - 上--previous 获取上一个  
    - 下--next 获取下一个 
    - 每次有输入调用append
    '''
    def __init__(self):
        self.index = 0
        self.history = []
    
    def next(self):
        '''
        获取下一条
        '''
        if len(self.history) == 0:
            return ""
        if self.index >= (len(self.history) - 1):
            # 已经到了最后一条
            return self.history[-1]
        self.index += 1
        return self.history[self.index]
    
    def previous(self):
        '''
        获取上一条
        '''
        if len(self.history) == 0:
            return ""
        if self.index <= 0:
            # 已经到了第一条
            return self.history[0]
        self.index -= 1
        return self.history[self.index]
    
    def append(self,cmd):
        '''
        添加新的
        '''
        self.history.append(cmd)
        # 如果长度超过了2000，把数组截断以下子
        if len(self.history) > 2000:
            self.history = self.history[1:2000]
        self.index = len(self.history)


# 输入历史
history = History()

def minput():
    msg = td_input()
    history.append(msg)
    return msg

