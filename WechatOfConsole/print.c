#include "print.h"
#include <stdio.h>
#include <sys/time.h>
#include <stdlib.h>
#include <signal.h>

int matrix[24][28] = {0};
int score,level;
int tm = 800000; // 0.8s

int n_x = 46;
int n_y = 8;
int n_num,n_mode,n_color;

extern int s_x,s_y,l_x,l_y;

//shape[][][16]:距离 右侧空格项  [17]:距离 下方空格项
int shape[7][4][18] = 
	{
		{
			{1,1,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,0, 2,2},
			{1,1,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,0, 2,2},
			{1,1,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,0, 2,2},
			{1,1,0,0, 1,1,0,0, 0,0,0,0, 0,0,0,0, 2,2},
		},
		{
			{1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 3,0},
			{1,1,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,3},
			{1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0, 3,0},
			{1,1,1,1, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,3},
		},
		{
			{0,1,0,0, 1,1,1,0, 0,0,0,0, 0,0,0,0, 1,2},
			{1,0,0,0, 1,1,0,0, 1,0,0,0, 0,0,0,0, 2,1},
			{1,1,1,0, 0,1,0,0, 0,0,0,0, 0,0,0,0, 1,2},
			{0,1,0,0, 1,1,0,0, 0,1,0,0, 0,0,0,0, 2,1}
		},
		{
			{1,1,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 1,2},
			{0,1,0,0, 1,1,0,0, 1,0,0,0, 0,0,0,0, 2,1},
			{1,1,0,0, 0,1,1,0, 0,0,0,0, 0,0,0,0, 1,2},
			{0,1,0,0, 1,1,0,0, 1,0,0,0, 0,0,0,0, 2,1},
		},
		{
			{0,1,1,0, 1,1,0,0, 0,0,0,0, 0,0,0,0, 1,2},
			{1,0,0,0, 1,1,0,0, 0,1,0,0, 0,0,0,0, 2,1},
			{0,1,1,0, 1,1,0,0, 0,0,0,0, 0,0,0,0, 1,2},
			{1,0,0,0, 1,1,0,0, 0,1,0,0, 0,0,0,0, 2,1},
		},
		{
			{0,0,1,0, 1,1,1,0, 0,0,0,0, 0,0,0,0, 1,2},
			{1,0,0,0, 1,0,0,0, 1,1,0,0, 0,0,0,0, 2,1},
			{1,1,1,0, 1,0,0,0, 0,0,0,0, 0,0,0,0, 1,2},
			{1,1,0,0, 1,0,0,0, 1,0,0,0, 0,0,0,0, 2,1}
		},
		{
			{1,0,0,0, 1,1,1,0, 0,0,0,0, 0,0,0,0, 1,2},
			{1,1,0,0, 1,0,0,0, 1,0,0,0, 0,0,0,0, 2,1},
			{1,1,1,0, 0,0,1,0, 0,0,0,0, 0,0,0,0, 1,2},
			{0,1,0,0, 0,1,0,0, 1,1,0,0, 0,0,0,0, 2,1}},
	};

//初始化图形的位置
int i_x = 24,i_y = 6;//init

//正在运动图形具体形状、颜色
int num,mode,color;
//正在运动图形的坐标
int x,y;

//指定位置输出 图形
void print_mode_shape(int n,int m,int x,int y,int c)
{
	int i = 0;
	int xx = x;
	int yy = y;
	for(;i < 16;i++){
		if(i != 0 && i%4 == 0){
			yy += 1;
			xx = x;
		}


		if(shape[n][m][i] == 1){
			printf("\33[%d;%dH\33[%dm[]\33[0m",yy,xx,c);
		}
		xx += 2;
	}
	fflush(NULL);
}

//输出下一图形
void print_next()
{
	eraser_shape(n_num,n_mode,n_x,n_y);

	n_num = random()%7;
	n_mode = random()%4;
	n_color = random()%7+40;

	//在指定位置输出图形
	print_mode_shape(n_num,n_mode,n_x,n_y,n_color);

	fflush(NULL);
}

void eraser_shape(int n,int m,int a,int b)
{
	int i = 0;
	int xx = a;
	int yy = b;

	for(i = 0;i < 16;i++){
		if(i != 0 && i%4 == 0){
			yy++;
			xx = a;
		}
		if(shape[n][m][i] == 1){
			printf("\33[%d;%dH  \33[0m",yy,xx);
		}
		xx += 2;
	}
	fflush(NULL);
}

//生成新图片
void init_shape()
{
	num = n_num;
	mode = n_mode;
	color = n_color;
	x = i_x;
	y = i_y;
	print_mode_shape(num,mode,x,y,color);
}

void store_shape()
{
	int m_x = y-6;
	int m_y = x-12;

	int i;
	for(i = 0;i < 16;i++){
		if(i != 0 && i%4 == 0){
			m_x++;
			m_y = x-12;
		}
		if(shape[num][mode][i] == 1){
			matrix[m_x][m_y] = color;
			matrix[m_x][m_y+1] = color;
		}
		m_y += 2;
	}
}

//碰撞检测，如果撞上返回1， 否则返回0
int judge_shape(int n,int m,int x,int y)
{
	//matrix[][];
	int m_x = y - 6;
	int m_y = x - 12;

	int i = 0;
	for(;i < 16;i++){
		if(i != 0 && i%4 == 0){
			m_x++;
			m_y = x-12;
		}

		if(shape[n][m][i] == 1){
			if(matrix[m_x][m_y] != 0){
				return 1;
			}
		}
		m_y += 2;
	}
	return 0;
}

//绘制图形显示窗体
void print_matrix()
{
	//printf("\33[20;60H print_matrix \33[0m");

	int i,j;
	for(i = 0;i < 24;i++){
		for(j = 0;j < 28;j += 2){
			if(matrix[i][j] == 0){
				printf("\33[%d;%dH  \33[0m",i+6,j+12);
			}else{
				printf("\33[%d;%dH\33[%dm[]\33[0m",i+6,j+12,matrix[i][j]);
			}
		}
	}
}

//输出分数  输出等级
void print_store_level()
{
	printf("\33[%d;%dH分数:%d\33[0m",s_y,s_x,score);
	printf("\33[%d;%dH等级:%d\33[0m",l_y,l_x,level);
	fflush(NULL);
}

//判断，然后消除整行
static void destroy_line()
{
	//遍历二维数组
	int i,j,k,flag;
	for(i = 0;i < 24;i++){
		flag = 1;//满行标志，如果为1满  0不满
		for(j = 0;j < 28;j++){
			if(matrix[i][j] == 0){
				flag = 0;
				break;
			}
		}
		//如果第i行是满的
		if(flag == 1){
			score += 10;
			if(score % 100 == 0){
				//修改等级，重新设置定时器
				level++;
				tm /= 2;
				alarm_us(tm);
			}
			//删除i行，整体下移
			for(k = i;k > 0;k--){
				for(j = 0;j < 28;j++){
					matrix[k][j] = matrix[k-1][j];
				}
			}
			print_matrix();
			print_store_level();
		}
	}
}

//
int move_down(int n,int m)
{
	if(y+(4-shape[n][m][17])-1 >= 29 ||
			judge_shape(n,m,x,y+1)){
		//已经触底  或 越界,不能再向下移动
		//保存图形
		store_shape();

		//消行
		destroy_line();

		//生成新图片
		init_shape();
		//生成下一个图片
		print_next();

		return 1;
	}

	//清除现有图形
	eraser_shape(n,m,x,y);
	y++;
	print_mode_shape(n,m,x,y,color);
	return 0;
}

//微妙定时器,定时器一旦启动，会每隔一段时间发送SIGALRM信号
void alarm_us(int n)
{
	struct itimerval value;
	//定时器启动的初始值
	value.it_value.tv_sec = 0;
	value.it_value.tv_usec = n;

	//定时器启动后的间隔时间值
	value.it_interval.tv_sec = 0;
	value.it_interval.tv_usec = n;

	setitimer(ITIMER_REAL,&value,NULL);
}

//SIGALRM 信号处理函数
void catch_signal(int s)
{
	//alarm(1);
	move_down(num,mode);
}

void fall_down()
{
	int i;
	while(1){
		i = move_down(num,mode);
		if(i == 1)
			return;
	}
}

int move_left(int n,int m)
{
	//边界检测
	if(x <= 12){
		return 1;
	}
	//碰撞检测
	if(judge_shape(n,m,x-2,y))
		return 1;

	//消除原有图形 左移一个单位重新绘制
	eraser_shape(n,m,x,y);
	x -= 2;
	print_mode_shape(n,m,x,y,color);
	
	return 0;
}
int move_right(int n,int m)
{
	//判断图形最右列 有没有越界
	if(x+2*(4-shape[n][m][16])-1 >= 39)
		return 1;
	if(judge_shape(n,m,x+2,y))
		return 1;

	//消除原有图形 左移一个单位重新绘制
	eraser_shape(n,m,x,y);
	x += 2;
	print_mode_shape(n,m,x,y,color);
	
	return 0;
}

//图形变换
int change_shape()
{
	int m = (mode+1)%4;
	//右侧越界判断
	if(x+2*(4-shape[num][m][16])-1 > 39)
		return 1;
	//下侧越界判断
	if(y+(4-shape[num][m][17])-1 > 29)
		return 1;

	eraser_shape(num,mode,x,y);
	mode = m;
	print_mode_shape(num,mode,x,y,color);
	return 0;
}

void game_over()
{
	printf("\33[32;9H**********  Game Over  ********\33[0m");
	//光标显示
	printf("\33[?25h");
	printf("\n\n");
}

void key_control()
{
	int ch;
	while(1){
		ch = getch();
		if(ch == ' '){
			//暂停、 继续
		}
		if(ch == 'q' || ch == 'Q'){
			break;
		}else if(ch == '\r'){//回车键
			//图形直接到底
			fall_down();
		}else if(ch == '\33'){// ^[[A  ^[[B ^[[C ^[[D
			ch = getch();
			if(ch == '['){
				ch = getch();
				switch(ch){
					case 'A':  //上
						change_shape();//shape[num][mode][i];
						break;
					case 'B':  //下
						move_down(num,mode);
						break;
					case 'C':  //右
						move_right(num,mode);
						break;
					case 'D':  //左
						move_left(num,mode);
						break;
					default:
						break;
				}
			}
		}
	}
	//游戏结束
	game_over();
}
