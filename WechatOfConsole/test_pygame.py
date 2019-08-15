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

# 保证输入模块的使用和input()函数没有区别！
#  重写输入模块： 遇到控制指令，直接处理，非控制指令，存入列表中。
#  输入backspace把最后一个元素移除。
#  每次有输入要打印
#  输入回车直接返回。

def getch():
    fd=sys.stdin.fileno() 
    old_settings=termios.tcgetattr(fd) 
    #old_settings[3]= old_settings[3] & ~termios.ICANON & ~termios.ECHO  
    try: 
        tty.setraw(fd) 
        ch=sys.stdin.read(1) 
    finally: 
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  
        #print 'error' 
    return ord(ch)

def td_print(*msgs,end="\n"):
    print(*msgs,end=end)
    sys.stdout.flush()

def td_input():
    td_print("\033[s",end="")  # 保存光标位置
    msg = []
    while True: 
        ch = getch()
        # print(ch)
        # print(type(ch))
        if ch== 3 : 
            #这个是ctrl-c 
            td_print()
            return ""
        if ch == 13: # 回车
            td_print()
            return "".join(msg)
        if ch == 127: # 删除最后一个字符
            if 0 != len(msg):
                msg.pop()
            td_print("\033[u",end="")  # 恢复光标位置 
            td_print("\033[K",end="")  # 从光标位置清空到行尾
            # td_print('\033[99999999999999D',end="") # 设置光标位置
            td_print("".join(msg),end="") # 内容回显
            continue

        if ch != 27: # 输入内容
            msg.append(chr(ch))
            td_print("\033[u",end="")  # 恢复光标位置 
            td_print("\033[K",end="")  # 从光标位置清空到行尾
            # td_print('\033[99999999999999D',end="") # 设置光标位置
            td_print("".join(msg),end="") # 内容回显
            continue
        
            

  
if __name__ == '__main__': 
    try:
        while True:
            td_print(">>>  ",end = '')
            cmd = td_input().strip() # 获取字符去除前后空格
            if cmd == '':    # 输入无效内容，直接跳过
                continue
            if cmd == 'exit':
                break
            # print(cmd)

    except Exception as e:
        print(e)
        #rate.sleep()

# BackSpace:127
# Enter: 13
# Esc: 27
# Ctrl-C: 3
# ↓: 27 91 66
# ↑: 27 91 65
# ←: 27 91 68
# →: 27 91 67
# 空格：32
# 输入的字符基本都是单个字符，而按键控制一般都是27开头的连续三四个字符




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

