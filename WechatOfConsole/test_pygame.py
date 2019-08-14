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
  
if __name__ == '__main__': 
    print ("Reading form keybord")
    print ('press Q to quit')
    while True: 
        fd=sys.stdin.fileno() 
        old_settings=termios.tcgetattr(fd) 
        #old_settings[3]= old_settings[3] & ~termios.ICANON & ~termios.ECHO  
        try: 
            tty.setraw(fd) 
            ch=sys.stdin.read(1) 
        finally: 
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  
            #print 'error' 
        print(ord(ch))
        if ord(ch)==0x3: 
            #这个是ctrl c 
            print ("shutdown")
            break
        #rate.sleep()