#include<stdio.h>
#include<conio.h>
#include<stdlib.h>
#include<windows.h>
#include<time.h>
#include<stdbool.h>
#include<stdint.h>

#define map_size 17//

#define UP	72//
#define DOWN	80
#define LEFT	75
#define	RIGHT	77

#define SNAKE 	3
#define FOOD 	2
#define WALL 	1

char map[map_size][map_size] = {0};
unsigned char food;
unsigned char snake[50] = {17};//初始化蛇座標
char length = 1;



void print_map() //印地圖
{
	for(int i = 0 ; i < 17 ; i++)
	{
		for(int j = 0 ; j < 17 ; j++)
		{
            if(map[i][j] == 0)
			{
				printf(" ");
			}
			else if(map[i][j] == SNAKE)
			{
				printf("o");
			}
			else if(map[i][j] == FOOD)
			{
				printf("@");
			}
			else if(map[i][j] == WALL)
			{
				printf("\033[38;2;255;255;0m█");

			}

		}
		printf("\033[0m\n");
		putchar('\n');
	}
	Sleep(500);//停止500毫秒
	system("cls");//清空螢幕
}


int get_direct(int old_direct)
{
	int new_direct = old_direct;//初始化新值為上一次的舊值，避免沒按鍵的情況
    if(_kbhit())//判斷有沒有按鍵
    {
        getch();//讀取按鍵值
        new_direct = getch();//新值設為按鍵值
    }
    if(length > 1)//蛇長大於1時避免按鍵是相反的
    {
        if(abs(new_direct - old_direct) == 8 || abs(new_direct - old_direct) == 2)//上下按鍵值差8，左右差2
        {
           return old_direct;
        }
    }


	return new_direct;

}


unsigned char random_food(){

    unsigned char food_,fx,fy;
    bool is_snake = false;


    do
    {
        is_snake = false;
        food_ = (unsigned char)(rand() % 256); // 0~255
        fx = food_ >> 4;
        fy = food_ & 0x0F;

        for(int i = 0 ; i < length ; i++)
        {
            if(food_ == snake[i])
            {
                is_snake = true;
            }
        }
    }
    while( fx == 0 || fx == 16 || fy == 0 || fy == 16 || is_snake);

    return food_;
}


void move_snake(int direct, unsigned char *food)
{
	int last = snake[0], current;//初始化last為蛇頭位置
	bool grow = false;
	unsigned char fx, fy, x, y;//fx, fy = food x, y座標 //x, y 蛇座標
	fx = *food >> 4;//利用二進位 右移4位計算x值
	fy = *food & 0x0F;//利用&運算符計算y值（十六進位 0x0F = 二進位 0000 1111）
	x = snake[0] >> 4;
	y = snake[0] & 0x0F;
	switch (direct)
	{
		case UP:
			y--;
			break;
		case DOWN:
			y++;
			break;
		case LEFT:
			x--;
			break;
		case RIGHT:
			x++;
			break;
	}
	snake[0] = (x << 4) | y;//利用二進位性質，將座標轉回十進位的值
	if(snake[0] == *food)//蛇吃到食物
	{
		grow = true;
		*food = random_food();
	}
	for(int i = 0 ; i < length ; i++)//蛇頭移動時，尾巴跟著動
	{
		if(i == 0)
		{
			continue;
		}
		current = snake[i];//尾巴座標先存到current
		snake[i] = last;//尾巴座標更新為蛇頭(前一位)座標(尾巴跑到蛇頭(前一位)位置)
		last = current;//尾巴原座標current變為下一輪的last
	}

	if(grow == true)
	{
		snake[length] = last;
		length++;
	}

	for(int i = 0 ; i < 17 ; i++)
	{
		for(int j = 0 ; j < 17 ; j++)
		{
			if(i == 0 || i == 16 || j == 0 || j ==16 )//牆
			{
				map[i][j] = WALL;
			}
			else if(i == fy && j == fx)//食物
			{
				map[i][j] = FOOD;
			}
			else
			{
				map[i][j] = 0;
			}
		}
	}
	for(int i = 0 ; i < length ; i++)//蛇
	{
		x = snake[i] >> 4;
		y = snake[i] &0x0F;
		if(snake[i] > 0)
		{
			map[y][x] = SNAKE;
		}
	}

}



bool is_alive()
{
    unsigned char x, y;
    x = snake[0] >> 4;
    y = snake[0] & 0x0F;

    return (x == 0 || x == 16 || y == 0 || y == 16) ? false : true;

}


int main()
{
	for(int i = 0 ; i < 17 ; i++)
	{
		for(int j = 0 ; j < 17 ; j++)
		{
			map[i][j] = 0;
		}
	}
	for(int i = 1 ; i < 50 ; i++)
	{
		snake[i] = 0;
	}

	int direct;
	bool Alive = true;
	srand((unsigned int)time(NULL));
    food = random_food();
	while(1)
	{
		print_map();
		direct = get_direct(direct);
		move_snake(direct, &food);
		Alive = is_alive();
		if(!Alive)
		{
			printf("Game over!\n");
			break;
		}

	}

	return 0;


}
