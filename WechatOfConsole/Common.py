# Authro     : ThreeDog
# Data       : 2019-06-12
# Function   : 共同包，存放一些公共的定义，主要是程序中用到文字转化的地方

from tdinput import td_input

# 消息类型，转化成对应的消息类型显示
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

# linux常用命令，用于防止用户误输入被发送到聊天
cmd_list = ['pwd','ls','cd','grep','touch','rm','exit','bye','rm','vi',':wq',':q!',':Q!','cat','cp','mv','rmdir','mk','git','cls','clear','find']

# 英文翻译
language = {}

# 群聊还是个人
user_type_dict = {
    'r':'【群聊】',
    'f':'【好友】',
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

