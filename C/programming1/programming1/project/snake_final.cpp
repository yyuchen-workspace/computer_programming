#include<stdio.h>
#include<conio.h>
#include<stdlib.h>
#include<windows.h>
#include<time.h>
#include<stdbool.h>
#include<stdint.h>

constexpr int map_size = 17;
constexpr int lazer_size = 17;

constexpr int snake_initial    = 77;
constexpr int computer_initial = 55;

constexpr int UP	 = 72;
constexpr int DOWN	 = 80;
constexpr int LEFT	 = 75;
constexpr int RIGHT = 77;

constexpr int LAZER    = 5;
constexpr int COMPUTER = 4;
constexpr int SNAKE    = 3;
constexpr int FOOD     = 2;
constexpr int WALL     = 1;


void print_map(unsigned char map[map_size][map_size], unsigned char head_x, unsigned char head_y)
 {

    for (int i = 0; i < map_size; i++)
    {
        for (int j = 0; j < map_size; j++)
        {
            if (map[i][j] == WALL)
            {
                printf("\033[48;2;255;199;6m  \033[0m"); // 橙色牆壁
            }
            else if(map[i][j] == LAZER)
            {
                printf("\033[48;2;255;255;0m  \033[0m");//黃色激光
            }
            else if(map[i][j] == COMPUTER)
            {
                printf("\033[48;2;255;0;255m  \033[0m");//電腦蛇
            }
            else if (map[i][j] == SNAKE)
            {
                if(i == head_y && j == head_x)
                {
                    printf("\033[48;2;0;125;255m  \033[0m"); // 青色蛇
                }
                else
                {
                    printf("\033[48;2;0;255;255m  \033[0m"); // 青色蛇
                }
            }
            else if (map[i][j] == FOOD)
            {
                printf("\033[48;2;255;0;0m  \033[0m"); // 紅色食物
            }

            else
            {
                printf("  "); // 空白
            }
        }
        printf("\n"); // 每行換行
    }
    Sleep(500);  // 停止 500 毫秒
    system("cls"); // 清屏
}



int get_direct(int old_direct, unsigned char *length)
{
	int new_direct = old_direct;//初始化新值為上一次的舊值，避免沒按鍵的情況
    if(_kbhit())//判斷有沒有按鍵
    {
        getch();//讀取按鍵值
        new_direct = getch();//新值設為按鍵值
    }

    if(*length > 1)//蛇長大於1時避免按鍵是相反的
    {
        if(abs(new_direct - old_direct) == 8 || abs(new_direct - old_direct) == 2)//上下按鍵值差8，左右差2
        {
           return old_direct;
        }
    }


	return new_direct;

}


unsigned char random_food(unsigned char *snake, unsigned char *computer, unsigned char length, unsigned char computer_length){

    unsigned char food_, fx, fy;
    bool is_snake, is_computer;


    do
    {
        is_snake = false;
        is_computer = false;
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
        for(int i = 0 ; i < computer_length ; i++)
        {
            if(food_ == computer[i])
            {
                is_computer = true;
            }
        }

    }
    while( fx == 0 || fx == map_size - 1 || fy == 0 || fy == map_size - 1 || is_snake || is_computer);

    return food_;
}


int if_hit_the_wall(int move, unsigned char computer_x, unsigned char computer_y)
{

    int dx[] = {0, 0, -1, 1};  // 上、下、左、右的x變化
    int dy[] = {-1, 1, 0, 0};  // 上、下、左、右的y變化
    int new_x = computer_x + dx[move];
    int new_y = computer_y + dy[move];
    bool valid_move = false;
    if (new_x > 0 && new_x < map_size - 2 && new_y > 0 && new_y < map_size - 2)
    {
        valid_move = true;
    }
    while(!valid_move)
    {
        move = rand() % 4;//0向上,1向下,2向左,3向右
        new_x = computer_x + dx[move];
        new_y = computer_y + dy[move];
        if (new_x > 0 && new_x < map_size - 2 && new_y > 0 && new_y < map_size - 2)
        {
            valid_move = true;
        }
    }

    return move;
}


int choose_move_toward_food(unsigned char computer_x, unsigned char computer_y, unsigned char fx, unsigned char fy) {
    if (abs(computer_x - fx) > abs(computer_y - fy)) {
        return (computer_x > fx) ? 2 : 3;  // 向左或向右
    } else {
        return (computer_y > fy) ? 0 : 1;  // 向上或向下
    }
}



void move_computer(unsigned char *food,
                   unsigned char fx, unsigned char fy,
                   unsigned char *snake, unsigned char *computer, const unsigned char *length,
                   unsigned char *computer_length, unsigned char map[map_size][map_size])
{
    int computer_last = computer[0], current;
    unsigned char computer_x, computer_y;
    computer_x = computer[0] >> 4;
    computer_y = computer[0] &0x0F;

    bool computer_grow = false;
    int move = choose_move_toward_food(computer_x, computer_y, fx, fy);
    move = if_hit_the_wall(move, computer_x, computer_y);  // 確保不撞牆或障礙


    switch(move)
    {
        case 0:
            computer_y--;
            break;
        case 1:
            computer_y++;
            break;
        case 2:
            computer_x--;
            break;
        case 3:
            computer_x++;
            break;
    }

    computer[0] = (computer_x << 4) | computer_y;

    if(computer[0] == *food)
    {
        computer_grow = true;
        *food = random_food(snake, computer, *length, *computer_length);
    }
    for(int i = 0 ; i < *computer_length ; i++)//蛇頭移動時，尾巴跟著動
	{
		if(i == 0)
		{
			continue;
		}
		current = computer[i];//尾巴座標先存到current
		computer[i] = computer_last;//尾巴座標更新為蛇頭(前一位)座標(尾巴跑到蛇頭(前一位)位置)
		computer_last = current;//尾巴原座標current變為下一輪的last
	}
	if(computer_grow == true)
	{
		computer[*computer_length] = computer_last;
		(*computer_length)++;
	}

}


void move_snake(int direct, unsigned char *food, unsigned char *head_x, unsigned char *head_y,
                unsigned char fx, unsigned char fy,
                unsigned char *snake, unsigned char *computer, unsigned char *length,
                unsigned char *computer_length, unsigned char map[map_size][map_size])
{
    bool snake_grow = false;
    int snake_last = snake[0], current;
    unsigned char x, y;
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
    *head_x = x;
    *head_y = y;
	snake[0] = (x << 4) | y;//利用二進位性質，將座標轉回十進位的值
	if(snake[0] == *food)//蛇吃到食物
	{
		snake_grow = true;
		*food = random_food(snake, computer, *length, *computer_length);
	}


	for(int i = 0 ; i < *length ; i++)//蛇頭移動時，尾巴跟著動
	{
		if(i == 0)
		{
			continue;
		}
		current = snake[i];//尾巴座標先存到current
		snake[i] = snake_last;//尾巴座標更新為蛇頭(前一位)座標(尾巴跑到蛇頭(前一位)位置)
		snake_last = current;//尾巴原座標current變為下一輪的last
	}
	if(snake_grow == true)
	{
		snake[*length] = snake_last;
		(*length)++;
	}

}


void hit_the_snake(unsigned char *snake, unsigned char *computer, unsigned char map[map_size][map_size], bool *win, bool *lose)
{
    unsigned char x, y, computer_x, computer_y;
    x = snake[0] >> 4;
    y = snake[0] &0x0F;
    computer_x = computer[0] >> 4;
    computer_y = computer[0] &0x0F;

    if(x == computer_x && y == computer_y)
    {
        *lose = true;
    }
    else if(map[y][x] == COMPUTER)
    {
        *lose = true;
    }
    else if(map[computer_y][computer_x] == SNAKE)
    {
        *win = true;
    }
}


void map_setting(const unsigned char *snake, const unsigned char *computer,
                 unsigned char fx, unsigned char fy,
                 const unsigned char *length, const unsigned char *computer_length, unsigned char map[map_size][map_size])
{

    unsigned char x, y, computer_x, computer_y;
    for(int i = 0 ; i < map_size ; i++)
	{
		for(int j = 0 ; j < map_size ; j++)
		{
			if(i == 0 || i == map_size - 1 || j == 0 || j == map_size - 1)//牆
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


	for(int i = 0 ; i < *length ; i++)//蛇
	{
		x = snake[i] >> 4;
		y = snake[i] &0x0F;
        if(snake[i] > 0)
		{
			map[y][x] = SNAKE;
		}
	}
	for(int i = 0 ; i < *computer_length ; i++)//蛇
	{
		computer_x = computer[i] >> 4;
		computer_y = computer[i] &0x0F;
        if(computer[i] > 0)
		{
			map[computer_y][computer_x] = COMPUTER;
		}
	}
}





void move_all(int direct, unsigned char *food, unsigned char *head_x, unsigned char *head_y,//fx, fy = food x, y座標 //x, y 蛇座標
                unsigned char *snake, unsigned char *computer, unsigned char *length, unsigned char *computer_length, unsigned char map[map_size][map_size], bool *win, bool *lose)
{
	unsigned char fx, fy;//fx, fy = food x, y座標 //x, y 蛇座標
    fx = *food >> 4;//利用二進位 右移4位計算x值
	fy = *food & 0x0F;//利用&運算符計算y值（十六進位 0x0F = 二進位 0000 1111）
    move_computer(food, fx, fy, snake, computer, length, computer_length, map);
    move_lazer();
    move_snake(direct, food, head_x, head_y, fx, fy, snake, computer, length, computer_length, map);
    hit_the_snake(snake, computer, map, win, lose);
	map_setting(snake, computer, fx, fy, length, computer_length, map);

}






bool snake_hit_the_wall(unsigned char *snake)
{
    bool dead = false;
    unsigned char x, y;
    x = snake[0] >> 4;
    y = snake[0] & 0x0F;

    if(x == 0 || x == map_size - 1 || y == 0 || y == map_size - 1)
    {
        dead = true;
    }

    return dead;
}


int main()
{
    unsigned char map[map_size][map_size] = {0};
    unsigned char food;
    unsigned char snake[50] = {snake_initial};//初始化蛇座標
    unsigned char computer[50] = {computer_initial};
    unsigned char length = 1;
    unsigned char computer_length = 1;



	for(int i = 0 ; i < map_size ; i++)
	{
		for(int j = 0 ; j < map_size ; j++)
		{
			map[i][j] = 0;
		}
	}
	for(int i = 1 ; i < 50 ; i++)
	{
		snake[i] = 0;
	}

	for(int i = 1 ; i < 50 ; i++)
	{
		computer[i] = 0;
	}

	int direct;
	unsigned char head_x = 1, head_y = 1;
	bool win = false, lose = false, dead = false;
	srand((unsigned int)time(NULL));
    food = random_food(snake, computer, length, computer_length);
	while(1)
	{
		print_map(map, head_x, head_y);
		direct = get_direct(direct, &length);
		move_all(direct, &food, &head_x, &head_y, snake, computer, &length, &computer_length, map, &win, &lose);
		dead = snake_hit_the_wall(snake);
		if(win)
		{
			printf("Excellent! You win!\n");
			break;
		}
		else if(lose || dead)
		{
			printf("Game over! You lose!\n");
			break;
		}

	}

	return 0;


}

