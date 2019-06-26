# Authro     : ThreeDog
# Data       : 2019-05-24
# Function   : 此模块提供用户调用的所有函数。用户输入 ls cd find 等命令均调用此模块的函数。
# Remark     : 调用方法通过getattr，即反射的形式实现调用。因此函数名很重要不可乱写
# 函数调用的操作对象均是用户列表，因此传入将users列表作为parent参数传入

from Common import cmd_list


class Cmd(object):
    def __init__(self,parent=None):
        self.parent = parent

    def ls(self,arg):
        '''
        获取最新消息列表
        '''
        if len(arg) == 0:         # ls 没有参数：获取所有消息列表
            if not self.parent.hasNewMsg():  # 没有新消息
                print("消息列表为空")
            else:
                for user in self.parent.getUsers():
                    if user.hasNewMsg(): # 消息列表必须不为空
                        # 如果消息列表不为空，就把这个人的消息都打印出来
                        print("【id:{:^3} 】 {:^10} 发来 {:^3} 条未读消息".format(user.id,user.getName(),len(user.msgs)))

        elif arg[0] == '-f':    # ls -f 好友列表
            print("好友列表：")
            for user in self.parent.getUsers():
                print(" {:^4}：{:^4} {:^3} ".format(user.id,user.type,user.getName()))
                
        else :
            print('参数错误，请重试')

    def cd(self,arg):
        '''
        进入聊天室， cd {id}  进入与id进行聊天的界面
        '''
        if len(arg) == 0 :
            print("cd命令需要参数")
            return
        elif arg[0] == '..':
            # 返回主页
            return
        else:
            try:
                user_id = int(arg[0])
            except Exception :
                print("cd后请输入一个数字")
                return 
            user = self.parent.getUserByID(user_id)
            self.parent.current_user = user
            self.cls(None)
            # 进入后先把队列中的消息打印
            while user.hasNewMsg():
                msg = user.takeMsg()
                print("【{}】{} ===> ：{}".format(msg.createTime,user.getName(),msg.text))
            # 进入与其聊天的死循环
            while True:
                print(" 与 {} 聊天中 >>> ".format(user.getName()),end = '')
                msg = input()
                if msg == 'cd ..':
                    # 退出聊天，把当前正在沟通的用户置为None
                    self.parent.current_user = None
                    break
                # 如果输入内容包含疑似cmd字符串，这个len不为0
                if len(list(filter(lambda x:True if x in msg else False,cmd_list))) > 0:
                    print("您的输入中包含疑似shell终端命令的字符串，确认发送此消息吗？y or n")
                    res = input()
                    if res == 'y' or res == 'yes':
                        pass
                    else:
                        continue 
                # 如果能走到这一步就发送数据
                self.parent.sendMsg(msg,user.userName) # 将信息发送给user  userName是微信用于识别的用户名

    def find(self,arg):
        '''
        通过字符串查找对象 , 命令示例： find 张三 李四 三级狗
        '''
        if len(arg) == 0:
            print("参数错误，请重试")
            return
        
        result = []
        print("查找到以下好友|群聊：")
        for keywords in arg:        # 列表拆分  关键字进行模糊查询
            for user in self.parent.getUsers():
                if keywords in user: # User的in重写过！
                    if user not in result: # 已经存在的不再添加防止重复
                        result.append(user)
        # x 就是每一个user
        # 注意map是一个惰性序列，必须要list一下才会执行
        list(map(lambda x : print(" {:^4}：{:^4} {:^4}  {:^4} ".format(x.id,x.type,x.remarkName,x.nickName)) ,result))

    def cls(self,arg): #清屏
        print("\033c",end='')
        
    def clear(self,arg): # 同上
        print("\033c",end='')
