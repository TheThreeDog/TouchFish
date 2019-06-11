# Authro     : ThreeDog
# Data       : 2019-05-24
# Function   : 此模块提供用户调用的所有函数。用户输入 ls cd find 等命令均调用此模块的函数。
# Remark     : 调用方法通过getattr，即反射的形式实现调用。因此函数名很重要不可乱写
# 函数调用的操作对象均是用户列表，因此传入将users列表作为parent参数传入

class Cmd(object):
    def __init__(self,parent=None):
        self.parent = parent

    def ls(self,arg):
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
        else :
            print('参数错误，请重试')

    def cd(self,arg):
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

    def find(self,arg):
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

    def cls(self,arg): #清屏
        print("\033c",end='')
