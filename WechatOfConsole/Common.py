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

# 支持的表情：
emoj_dict = {
    "emoj1" : "[微笑]",
    "emoj2" : "[撇嘴]",
    "emoj3" : "[色]",
    "emoj4" : "[发呆]",
    "emoj5" : "[得意]",
    "emoj6" : "[流泪]",
    "emoj7" : "[害羞]",
    "emoj8" : "[闭嘴]",
    "emoj9" : "[睡]",
    "emoj10" : "[大哭]",
    "emoj11" : "[尴尬]",
    "emoj12" : "[调皮]",
    "emoj13" : "[呲牙]",
    "emoj14" : "[惊讶]",
    "emoj15" : "[难过]",
    "emoj16" : "[囧]",
    "emoj17" : "[抓狂]",
    "emoj18" : "[吐]",
    "emoj19" : "[偷笑]",
    "emoj20" : "[愉快]",
    "emoj21" : "[白眼]",
    "emoj22" : "[傲慢]",
    "emoj23" : "[困]",
    "emoj24" : "[惊恐]",
    "emoj25" : "[流汗]",
    "emoj26" : "[憨笑]",
    "emoj27" : "[悠闲]",
    "emoj28" : "[奋斗]",
    "emoj29" : "[咒骂]",
    "emoj30" : "[疑问]",
    "emoj31" : "[嘘]",
    "emoj32" : "[晕]",
    "emoj33" : "[衰]",
    "emoj34" : "[敲打]",
    "emoj35" : "[再见]",
    "emoj36" : "[擦汗]",
    "emoj37" : "[抠鼻]",
    "emoj38" : "[鼓掌]",
    "emoj39" : "[坏笑]",
    "emoj40" : "[左哼哼]",
    "emoj41" : "[右哼哼]",
    "emoj42" : "[哈欠]",
    "emoj43" : "[鄙视]",
    "emoj44" : "[委屈]",
    "emoj45" : "[快哭了]",
    "emoj46" : "[阴险]",
    "emoj47" : "[亲亲]",
    "emoj48" : "[可怜]",
    "emoj49" : "[菜刀]",
    "emoj50" : "[西瓜]",
    "emoj51" : "[啤酒]",
    "emoj52" : "[咖啡]",
    "emoj53" : "[猪头]",
    "emoj54" : "[玫瑰]",
    "emoj55" : "[凋谢]",
    "emoj56" : "[嘴唇]",
    "emoj57" : "[爱心]",
    "emoj58" : "[心碎]",
    "emoj59" : "[蛋糕]",
    "emoj60" : "[炸弹]",
    "emoj61" : "[便便]",
    "emoj62" : "[月亮]",
    "emoj63" : "[太阳]",
    "emoj64" : "[拥抱]",
    "emoj65" : "[强]",
    "emoj66" : "[弱]",
    "emoj67" : "[握手]",
    "emoj68" : "[胜利]",
    "emoj69" : "[抱拳]",
    "emoj70" : "[勾引]",
    "emoj71" : "[拳头]",
    "emoj72" : "[OK]",
    "emoj73" : "[跳跳]",
    "emoj74" : "[发抖]",
    "emoj75" : "[怄火]",
    "emoj76" : "[转圈]",
    "emoj77" : "😄",
    "emoj78" : "😷",
    "emoj79" : "😂",
    "emoj80" : "😝",
    "emoj81" : "😳",
    "emoj82" : "😱",
    "emoj83" : "😔",
    "emoj84" : "😒",
    "emoj85" : "[嘿哈]",
    "emoj86" : "[捂脸]",
    "emoj87" : "[奸笑]",
    "emoj88" : "[机智]",
    "emoj89" : "[皱眉]",
    "emoj90" : "[耶]",
    "emoj91" : "[吃瓜]",
    "emoj92" : "[加油]",
    "emoj93" : "[汗]",
    "emoj94" : "[天啊]",
    "emoj95" : "[天啊]",
    "emoj96" : "[Emm]",
    "emoj97" : "[社会社会]",
    "emoj98" : "[旺柴]",
    "emoj99" : "[好的]",
    "emoj100" : "[打脸]",
    "emoj101" : "[哇]",
    "emoj102" : "[红包]",
    "emoj103" : "[發]",
    "emoj104" : "[福]",
    "emoj105" : "👻",
    "emoj106" : "🙏",
    "emoj107" : "💪",
    "emoj108" : "🎉",
    "emoj109" : "📦"
}

emoj_list = list(emoj_dict.values())

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

