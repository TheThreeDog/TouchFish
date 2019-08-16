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

# 保证输入模块的使用和input()函数没有区别！
#  重写输入模块： 遇到控制指令，直接处理，非控制指令，存入列表中。
#  输入backspace把最后一个元素移除。
#  每次有输入要打印
#  输入回车直接返回。

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


def register_func(cmd): # 注册装饰器， 使用方法 @register_func()
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

@register_func(CmdType.CMD_CTRL_C)
def ctrl_c():
    td_print("^C")
    return ""

def td_input():
    td_print("\033[s",end="")  # 保存光标位置
    msg = []
    try:
        while True: 
            ch = getch()
            # print(type(ch))
            if ch== 3 : 
                #这个是ctrl-c  直接返回，效果上则是丢弃了当前行的内容。                
                return func_dict[CmdType.CMD_CTRL_C]()

            if ch == 13: # 回车
                td_print()
                return "".join(msg)
            if ch == 127: # 删除最后一个字符
                if 0 != len(msg):
                    msg.pop()
                td_flush(msg)
                continue 
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
            else : # 输入内容
                msg.append(chr(ch))
                td_flush(msg)
                continue
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

