#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>
#include<time.h>
#include<windows.h>
#include<conio.h>


constexpr int32_t WALL = 1;
constexpr int32_t FOOD = 2;
constexpr int32_t SNAKE= 3;
constexpr int32_t map_row = 32;
constexpr int32_t map_column = 64;

constexpr int32_t UP = 72;
constexpr int32_t DOWN = 80;
constexpr int32_t LEFT = 75;
constexpr int32_t RIGHT = 77;



int32_t map[map_row][map_column] = {0};
int32_t snake_x[100] = {0}, snake_y[100] = {0};
int32_t direct = 0;
int32_t length = 1;


//map
void print_map()
{
    

    srand(time(0));
   



    for(int i = 0  ; i < map_row ; i++)
    {
        for(int j = 0 ; j < map_column ; j++)
        {
            if(i == 0 || i == map_row - 1 || j == 0 || j == map_column - 1)
            {
                printf("#");
            }
            else if(map[i][j] == FOOD)
            {
                printf("@");
            }
            else if(map[i][j] == SNAKE)
            {
                printf("o");
            }
            else
            {
                printf(" ");
            }
        }
        printf("\n");
    }
    Sleep(500);
    system("cls");

}


int32_t get_direct(int32_t old_direct)
{
	int32_t new_direct = old_direct;//初始化新值為上一次的舊值，避免沒按鍵的情況
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


int32_t food_isolation(){

    unsigned char food_,fx,fy;
    bool is_snake = false;


    do
    {
        is_snake = false;
        food_ = (unsigned char)(rand() % 256); // 0~255

        for(int i = 0 ; i < length ; i++)
        {
            if(food_ == snake_x[i] * snake_y[i])
            {
                is_snake = true;
            }
        }
    }
    while( fx == 0 || fx == 16 || fy == 0 || fy == 16 || is_snake);

    return food_;
}


void move_snake(int32_t direct, int32_t food)
{
    int32_t last = snake_x[0] * snake_y[0] , current;//初始化last為蛇頭位置
	bool grow = false;

    int32_t fx, fy, x, y;//x表示map[row], y表示map[column]

	switch (direct)
	{
		case UP:
			x--;
			break;
		case DOWN:
			x++;
			break;
		case LEFT:
			y--;
			break;
		case RIGHT:
			y++;
			break;
	}
	snake_x[0] = x;//利用二進位性質，將座標轉回十進位的值
    snake_y[0] = y;
	if(snake_x[0] * snake_y[0] == food)//蛇吃到食物
	{
		grow = true;
		food = food_isolation();
	}
	for(int i = 0 ; i < length ; i++)//蛇頭移動時，尾巴跟著動
	{
		if(i == 0)
		{
			continue;
		}
		current = snake_x[i] * snake_y[];//尾巴座標先存到current
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
		
		if(snake[i] > 0)
		{
			map[y][x] = SNAKE;
		}
	}
}


int main()
{
    for(int i = 0 ; i < map_row ; i++)
    {
        for(int j = 0 ; j < map_column ; j++)
        {
            map[i][j] = 0;
        }
    }


    bool Alive = true;
    print_map();
    direct = get_direct();
    snake_move();
    food_isolation();
    Alive = is_alive;
    if(!Alive)
    {

    }

}