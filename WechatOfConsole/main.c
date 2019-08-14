#include <stdio.h> //printf();
#include <termios.h>
#include "print.h"
#include <signal.h> 
#include <time.h>

int s_x = 9+2+28+1+5;//s: score		45
int s_y = 4+1+6+5+2; //				18
int l_x = 9+2+28+1+5;//l: level		45
int l_y = 4+1+6+5+4+2;//			22

//获取一个字符，不回显
int getch()
{
	struct termios tm,tm_old;
	//保存正常  输入属性 到 tm_old
	tcgetattr(0,&tm_old);
	//获取原始输入属性
	cfmakeraw(&tm);
	//设置原始输入属性
	tcsetattr(0,0,&tm);
	//不回显的获取一个字符
	int ch = getchar();
	//恢复正常输入属性
	tcsetattr(0,0,&tm_old);

	return ch;
}

//函数定义
void print_start_interface()
{
	//清屏
	printf("\33[2J");
	int i;
	//输出 最顶行、最低行
	for(i = 0;i < 47;i++){
		printf("\33[%d;%dH\33[43m \33[0m",5,i+10);
		printf("\33[%d;%dH\33[43m \33[0m",30,i+10);
	}
	//输出三列
	for(i = 0;i < 26;i++){
		printf("\33[%d;%dH\33[43m  \33[0m",i+5,10);
		printf("\33[%d;%dH\33[43m  \33[0m",i+5,40);
		printf("\33[%d;%dH\33[43m  \33[0m",
				i+5,56);
	}
	//输出  分数、下一图形分割行
	for(i=0;i < 17;i++){
		printf("\33[%d;%dH\33[43m \33[0m",12,40+i);
	}
								// 18  45
	printf("\33[%d;%dH分数:\33[0m",s_y,s_x);
								// 22  45
	printf("\33[%d;%dH等级:\33[0m",l_y,l_x);

	fflush(NULL);
}

void init_game()
{

	//输出窗体界面
	print_start_interface();

	//等待用户输入，然后程序开始运行
	getch();

	//获取随机数
	//设置随机数种子
	srand(time(NULL));
	// random()%(max-min+1) + min;
	num = random()%7;
	mode = random()%4;
	color = random()%7+40;

	x = i_x;
	y = i_y;

	//生成图形
	print_mode_shape(num,mode,x,y,color);

	print_next();
	printf("\33[?25l");
}

int main()
{
	init_game();

	//信号注册
	signal(SIGALRM,catch_signal);

	//开启定时器
	alarm_us(tm);
	//alarm(1);

	//监听 用户键盘操作
	key_control();

	return 0;
}
