# Authro     : ThreeDog
# Data       : 2019-06-12
# Function   : 翻译模块
import json

class Translator(object):
    '''
    翻译模块 做成一个单例，整个代码仅使用一个实例。
    '''
    def __init__(self):
        self.transList = []
    
    def load(self,filePath):
        # 加载翻译，将目标文件按照json格式全部转化为字典
        try:
            with open(filePath) as f:
                self.transList = json.loads(f.read())
        except FileNotFoundError:
            print("翻译文件不存在：{}，请执行lupdate生成翻译文件。".format(filePath))
            exit(-1)

    def translate(self,srcStr):
        for json in self.transList:
            #
            #   字符串中有{}占位符替换的情况这里暂时没有考虑
            #
            if srcStr == json['msgid']:
                return json['msgstr']
        return srcStr

    def tr(self,srcStr):
        return self.translate(srcStr)

translator = Translator()

def tdtr(srcStr):
    return translator.tr(srcStr)
    