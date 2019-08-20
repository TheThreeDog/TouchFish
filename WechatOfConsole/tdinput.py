# import pygame

# def main():
#     pygame.init()
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN: #键被按下
#                 if event.key == pygame.K_LEFT:
#                     print("LEFT")
#                 elif event.key == pygame.K_RIGHT:
#                     print("RIGHT")
#                 elif event.key == pygame.K_UP:
#                     print("UP")
#                 elif event.key == pygame.K_DOWN:
#                     print("DOWN")
#             elif event.type == pygame.KEYUP:
#                 pass

# if __name__ == '__main__':
#     main()








# import sys, os
# from pynput.keyboard import Controller,Key,Listener
 
# # 监听按压
# def on_press(key):
#     try:
#         print("正在按压:",format(key.char))
#     except AttributeError:
#         print("正在按压:",format(key))
 
# # 监听释放
# def on_release(key):
#     print("已经释放:",format(key))
 
#     if key==Key.esc:
#         # 停止监听
#         return False
 
# # 开始监听
# def start_listen():
#     with Listener(on_press=on_press,on_release=on_release) as listener:
#         listener.join()
 
# if __name__ == '__main__':
 
#     # 实例化键盘
#     kb=Controller()
 
#     # 使用键盘输入一个字母
#     kb.press('a')
#     kb.release('a')
 
#     # 使用键盘输入字符串,注意当前键盘调成英文
#     kb.type("hello world")
 
#     # 使用Key.xxx输入
#     kb.press(Key.space)
 
#     # 开始监听,按esc退出监听
#     start_listen()



import os  
import sys 
import tty, termios 
import time   
from enum import Enum,unique


widths = [
    (126,  1), (159,  0), (687,   1), (710,  0), (711,  1),
    (727,  0), (733,  1), (879,   0), (1154, 1), (1161, 0),
    (4347,  1), (4447,  2), (7467,  1), (7521, 0), (8369, 1),
    (8426,  0), (9000,  1), (9002,  2), (11021, 1), (12350, 2),
    (12351, 1), (12438, 2), (12442,  0), (19893, 2), (19967, 1),
    (55203, 2), (63743, 1), (64106,  2), (65039, 1), (65059, 0),
    (65131, 2), (65279, 1), (65376,  2), (65500, 1), (65510, 2),
    (120831, 1), (262141, 2), (1114109, 1),
]

def get_width( o ):
    """Return the screen column width for unicode ordinal o."""
    """获取该字符在屏幕上的显示的长度"""
    global widths
    if o == 0xe or o == 0xf:
        return 0
    for num, wid in widths:
        if o <= chr(num):
            return wid
    return 1


#  保证输入模块的使用和input()函数没有区别！
#  重写输入模块： 遇到控制指令，直接处理，非控制指令，存入列表中。
#  输入backspace把最后一个元素移除。
#  每次有输入要打印
#  输入回车直接返回。
#  采用VT10编码控制
@unique # 不允许出现值相同的变量 
class CmdType(Enum):
    """
    这个类提供所有可用的按键键值的枚举类型
    键值对照：
    # BackSpace:127
    # Enter: 13
    # Esc: 27
    # Ctrl-C: 3
    # ↓: 27 91 66
    # ↑: 27 91 65
    # ←: 27 91 68
    # →: 27 91 67
    # 空格：32
    # 此枚举中仅记录常用的控制指令，其他字符很可能是输入字符因此不记录在此出以免影响输入
    # 
    """
    
    CMD_CTRL_A      =1
    CMD_CTRL_B      =2
    CMD_CTRL_C      =3
    CMD_CTRL_D      =4
    CMD_CTRL_E      =5
    CMD_CTRL_F      =6
    CMD_CTRL_G      =7
    CMD_CTRL_H      =8
    CMD_CTRL_I      =9
    CMD_CTRL_J      =10
    CMD_CTRL_K      =11
    CMD_CTRL_L      =12
    # CMD_CTRL_M      =13  #Linux存在键值相同的情况，比如回车和Ctrl-M都是13 因此只保留CMD_ENTER
    CMD_ENTER       =13
    CMD_CTRL_N      =14
    CMD_CTRL_O      =15
    CMD_CTRL_P      =16
    CMD_CTRL_Q      =17
    CMD_CTRL_R      =18
    CMD_CTRL_S      =19
    CMD_CTRL_T      =20
    CMD_CTRL_U      =21
    CMD_CTRL_V      =22
    CMD_CTRL_W      =23
    CMD_CTRL_X      =24
    CMD_CTRL_Y      =25
    CMD_CTRL_Z      =26
    CMD_ESC         =27
    CMD_SPACE       =32
    CMD_BACKSPACE   =127
    CMD_UP          =279165
    CMD_DOWN        =279166
    CMD_LEFT        =279168
    CMD_RIGHT       =279167
    CMD_INSERT      =279150126
    CMD_HOME        =279172
    CMD_PAGE_UP     =279153126
    CMD_PAGE_DOWN   =279154126
    CMD_DELETE      =279151126
    CMD_END         =279170

    @classmethod
    def getItem(cls,key):
        '''
        可以通过下标获取
        '''
        for name, member in cls.__members__.items():
            if member.value == key:
                return member
        raise (KeyError)
        



def getch():
    fd=sys.stdin.fileno() 
    old_settings=termios.tcgetattr(fd) 
    #old_settings[3]= old_settings[3] & ~termios.ICANON & ~termios.ECHO  
    try: 
        tty.setraw(fd) 
        ch=sys.stdin.read(1) 
    finally: 
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  
    return ord(ch)


"""
输入控制类，三级狗自研输入引擎，所有的输入前都由此控制，手动实现上下左右按键触发，指令触发和输入回显的逻辑！
"""
# 需求： 需要一个列表存储正在输入的数据
# 有一个下标记录当前光标的位置
msg = []
index = 0
position = 0 # 位置和下标不一样，下标代表正在操作的是第几个字符，位置代表在在终端中显示的位置。
length = 0

def update_position():
    global msg, index, position, length
    if index == 0:
        position = 0
    else:
        position = 0
        for ch in msg[0:index]:
            position += get_width(ch)


# 自动刷新装饰器，用于输入的函数，每次敲击字符后立马回显
def auto_flush(func):
    def inner(*args,**kwargs):
        f = func(*args,**kwargs)
        sys.stdout.flush()
        return f
    return inner
    
@auto_flush
def td_print(*msgs,end="\n"):
    print(*msgs,end=end)

@auto_flush
def td_flush(msg):
    print("\033[u",end="")  # 恢复光标位置 
    print("\033[K",end="")  # 从光标位置清空到行尾
    print("".join(msg),end="") # 内容回显

func_dict = {}

def default_handler():
    '''
    默认的处理方式：不处理
    '''
    pass

def init_func_dict():
    for member in CmdType.__members__.values():
        func_dict[member] = default_handler

init_func_dict()

def register_func(cmd): # 注册装饰器， 使用方法 @register_func(CmdType.CMD_XX_XX)
    def outer(func):
        if cmd not in CmdType:
            td_print("注册类型错误！CmdType中不包含此类型，请在类中添加")
            exit(-1)
        func_dict[cmd] = func 
        def register(*args,**kwargs):
            return func(*args,**kwargs)
        return register
    return outer

@register_func(CmdType.CMD_UP)
def up():
    td_print("按了↑箭头")

@register_func(CmdType.CMD_DOWN)
def down():
    td_print("按了↓箭头")

@register_func(CmdType.CMD_LEFT)
def left():
    td_print("\033[1D",end="") # 左移光标

@register_func(CmdType.CMD_RIGHT)
def right():
    td_print("\033[1C",end="") # 右移光标

@register_func(CmdType.CMD_CTRL_C)
def ctrl_c():#这个是ctrl-c  直接返回，效果上则是丢弃了当前行的内容。           
    td_print("^C")
    return ""

def td_input():
    td_print("\033[s",end="")  # 保存光标位置
    msg = []
    try:
        while True: 
            ch = getch()
            if ch == 3: # ctrl-c
                return func_dict[CmdType.CMD_CTRL_C]()

            if ch == 13: # 回车
                td_print()
                return "".join(msg)

            if ch == 27:        # 控制指令
                ch = getch()
                if ch == 91 :
                    ch = getch()
                    if ch == 65 : # ↑
                        func_dict[CmdType.CMD_UP]()
                    if ch == 66 : # ↓
                        func_dict[CmdType.CMD_DOWN]()
                    if ch == 67 : # →
                        func_dict[CmdType.CMD_RIGHT]()
                    if ch == 68 : # ←
                        func_dict[CmdType.CMD_LEFT]()
                    if ch == 70 : # END
                        func_dict[CmdType.CMD_END]()
                    if ch == 72 : # HOME
                        func_dict[CmdType.CMD_HOME]()
                    if ch == 50:  # INSERT
                        ch = getch()
                        if ch == 126:
                            func_dict[CmdType.CMD_INSERT]()
                        continue
                    if ch == 51:  # DELETE
                        ch = getch()
                        if ch == 126:
                            func_dict[CmdType.CMD_DELETE]()
                        continue
                    if ch == 53:  # PAGE_UP
                        ch = getch()
                        if ch == 126:
                            func_dict[CmdType.CMD_PAGE_UP]()
                        continue
                    if ch == 54:  # PAGE_DOWN
                        ch = getch()
                        if ch == 126:
                            func_dict[CmdType.CMD_PAGE_DOWN]()
                        continue
                    continue
                continue

            # 其余范围1~27的，直接调用
            if ch in range(1,28):
                func_dict[CmdType.getItem(ch)]()
                continue

            elif ch == 127: # 删除最后一个字符
                if 0 != len(msg):
                    msg.pop()
                td_flush(msg)
                continue 

            else : # 输入内容
                msg.append(chr(ch))
                td_flush(msg)
                continue
        return ""
    except KeyError as e:
        td_print(e)
        td_print("键值错误！尚未给此控制指令注册回调函数，请使用@register_func注册再调用")
    
if __name__ == '__main__': 

    try:
        while True:
            td_print(">>> ",end = '')
            cmd = td_input().strip() # 获取字符去除前后空格
            if cmd == '':    # 输入无效内容，直接跳过
                continue
            if cmd == 'exit':
                break
            # print(cmd)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        td_print(exc_type, fname, exc_tb.tb_lineno)
        #rate.sleep()





######################################################################3
# def td_input():
#     td_print("\033[s",end="")  # 保存光标位置
#     msg = []
#     while True: 
#         ch = getch()
#         # print(ch)
#         # print(type(ch))
#         if ch== 3 : 
#             #这个是ctrl-c 
#             td_print()
#             return ""
#         if ch == 13: # 回车
#             td_print()
#             return "".join(msg)
#         if ch == 127: # 删除最后一个字符
#             if 0 != len(msg):
#                 msg.pop()
#             #td_print("\033[u",end="")  # 恢复光标位置 # 清空本行
#             td_print("\033[2K",end="") # 清空本行
#             td_print('\033[99999999999999D',end="") # 设置光标位置
#             td_print(">>> ","".join(msg),end="") # 内容回显
#             continue

#         if ch != 27: # 输入内容
#             msg.append(chr(ch))
#             td_print("\033[2K",end="") # 清空本行
#             td_print('\033[99999999999999D',end="") # 设置光标位置
#             td_print(">>> ","".join(msg),end="") # 内容回显
#             continue

