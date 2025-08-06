#include "snake_function.h"

void print_map(unsigned char (*map)[map_size], int size, unsigned char head_x, unsigned char head_y)
 {

    for (int i = 0; i < map_size; i++)
    {
        for (int j = 0; j < map_size; j++)
        {
            if (map[i][j] == WALL)
            {
                printf("\033[48;2;255;199;6m  \033[0m"); // ������
            }
            else if(map[i][j] == LAZER)
            {
                printf("\033[48;2;255;255;0m  \033[0m");//����E��
            }
            else if(map[i][j] == COMPUTER)
            {
                printf("\033[48;2;255;0;255m  \033[0m");//�q���D
            }
            else if (map[i][j] == SNAKE)
            {
                if(i == head_y && j == head_x)
                {
                    printf("\033[48;2;0;125;255m  \033[0m"); // �C��D
                }
                else
                {
                    printf("\033[48;2;0;255;255m  \033[0m"); // �C��D
                }
            }
            else if (map[i][j] == FOOD)
            {
                printf("\033[48;2;255;0;0m  \033[0m"); // ���⭹��
            }

            else
            {
                printf("  "); // �ť�
            }
        }
        printf("\n"); // �C�洫��
    }
    Sleep(500);  // ���� 500 �@��
    system("cls"); // �M��
}



int get_direct(int old_direct, unsigned char *length)
{
	int new_direct = old_direct;//��l�Ʒs�Ȭ��W�@�����­ȡA�קK�S���䪺���p
    if(_kbhit())//�P�_���S������
    {
        getch();//Ū�������
        new_direct = getch();//�s�ȳ]�������
    }

    if(*length > 1)//�D���j��1���קK����O�ۤϪ�
    {
        if(abs(new_direct - old_direct) == 8 || abs(new_direct - old_direct) == 2)//�W�U����Ȯt8�A���k�t2
        {
           return old_direct;
        }
    }


	return new_direct;

}


unsigned char random_food(unsigned char *snake, unsigned char *computer, unsigned char length, unsigned char computer_length, int size){

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
    while( fx == 0 || fx == size - 1 || fy == 0 || fy == size - 1 || is_snake || is_computer);

    return food_;
}


void if_hit_the_wall(int *move, unsigned char computer_x, unsigned char computer_y, int size)
{

    int dx[] = {0, 0, -1, 1};  // �W�B�U�B���B�k��x�ܤ�
    int dy[] = {-1, 1, 0, 0};  // �W�B�U�B���B�k��y�ܤ�
    int new_x = computer_x + dx[*move];
    int new_y = computer_y + dy[*move];
    bool valid_move = false;
    if (new_x > 0 && new_x < size - 1 && new_y > 0 && new_y < size - 1)
    {
        valid_move = true;
    }
    while(!valid_move)
    {
        *move = rand() % 4;//0�V�W,1�V�U,2�V��,3�V�k
        new_x = computer_x + dx[*move];
        new_y = computer_y + dy[*move];
        if (new_x > 0 && new_x < size - 1 && new_y > 0 && new_y < size - 1 )
        {
            valid_move = true;
        }
    }
}


int choose_move_toward_food(unsigned char computer_x, unsigned char computer_y, unsigned char fx, unsigned char fy) {
    if (abs(computer_x - fx) > abs(computer_y - fy)) {
        return (computer_x > fx) ? 2 : 3;  // �V���ΦV�k
    } else {
        return (computer_y > fy) ? 0 : 1;  // �V�W�ΦV�U
    }
}



void move_computer(int *move, unsigned char *food,
                   unsigned char fx, unsigned char fy,
                   unsigned char *snake, unsigned char *computer, const unsigned char *length,
                   unsigned char *computer_length, unsigned char (*map)[map_size], int size)
{
    int computer_last = computer[0], current;
    unsigned char computer_x, computer_y;
    computer_x = computer[0] >> 4;
    computer_y = computer[0] &0x0F;

    bool computer_grow = false;
    *move = choose_move_toward_food(computer_x, computer_y, fx, fy);
    if_hit_the_wall(move, computer_x, computer_y, map_size);  // �T�O������λ�ê


    switch(*move)
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
        *food = random_food(snake, computer, *length, *computer_length, map_size);
    }
    for(int i = 0 ; i < *computer_length ; i++)//�D�Y���ʮɡA���ڸ�۰�
	{
		if(i == 0)
		{
			continue;
		}
		current = computer[i];//���ڮy�Х��s��current
		computer[i] = computer_last;//���ڮy�Ч�s���D�Y(�e�@��)�y��(���ڶ]��D�Y(�e�@��)��m)
		computer_last = current;//���ڭ�y��current�ܬ��U�@����last
	}
	if(computer_grow == true)
	{
		computer[*computer_length] = computer_last;
		(*computer_length)++;
	}

}


void move_lazer(const unsigned char *snake, unsigned char *lazer, int *lazer_time,
                const unsigned char *length, const unsigned char *computer_length, unsigned char *lazer_length, unsigned char (*map)[map_size], int size)
{
    if (*lazer_time == 5)
    {
        unsigned char x, y, lazer_x, lazer_y;
        int horizontal_or_vertical;
        bool OK;
        if(*length >= 25)
        {
            *lazer_length = 5;
        }

        do
        {
            OK = true;
            lazer[0] = (unsigned char)(rand() % 256); // 0~255
            x = snake[0] >> 4;
            y = snake[0] & 0x0F;
            lazer_x = lazer[0] >> 4;
            lazer_y = lazer[0] & 0x0F;
            horizontal_or_vertical = rand() % 2; // 0�����A1����

            for (int i = 1; i < *lazer_length; i++)
            {
                if (horizontal_or_vertical == 0)
                { // ����
                    lazer[i] = lazer[i - 1] + 16;
                }
                else
                { // ����
                    lazer[i] = lazer[i - 1] + 1;
                }

                lazer_x = lazer[i] >> 4;
                lazer_y = lazer[i] & 0x0F;

                if (lazer_x >= size || lazer_y >= size || map[lazer_y][lazer_x] != 0 || (lazer_x == x && lazer_y == y))
                {
                    OK = false;
                    break;
                }
            }
        } while (!OK);
    }

    *lazer_time -= 1;
    if (*lazer_time == 0)
    {
        *lazer_time = 5;
    }
}


void move_snake(int direct, unsigned char *food, unsigned char *head_x, unsigned char *head_y,
                unsigned char fx, unsigned char fy,
                unsigned char *snake, unsigned char *computer, unsigned char *length,
                unsigned char *computer_length, unsigned char (*map)[map_size], int size)
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
	snake[0] = (x << 4) | y;//�Q�ΤG�i��ʽ�A�N�y����^�Q�i�쪺��
	if(snake[0] == *food)//�D�Y�쭹��
	{
		snake_grow = true;
		*food = random_food(snake, computer, *length, *computer_length, map_size);
	}


	for(int i = 0 ; i < *length ; i++)//�D�Y���ʮɡA���ڸ�۰�
	{
		if(i == 0)
		{
			continue;
		}
		current = snake[i];//���ڮy�Х��s��current
		snake[i] = snake_last;//���ڮy�Ч�s���D�Y(�e�@��)�y��(���ڶ]��D�Y(�e�@��)��m)
		snake_last = current;//���ڭ�y��current�ܬ��U�@����last
	}
	if(snake_grow == true)
	{
		snake[*length] = snake_last;
		(*length)++;
	}

}


void hit_the_snake_or_lazer(unsigned char *snake, unsigned char *computer, unsigned char *length, unsigned char *computer_length, unsigned char (*map)[map_size], int size, bool *win, bool *lose)
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
    else if(map[y][x] == LAZER)
    {
        *lose = true;
    }
    else if(map[computer_y][computer_x] == SNAKE)
    {
        int temp = *computer_length;
        *length += *computer_length;
        *computer_length = 1;
        for(int i = 1 ; i < temp ; i++)
        {
            computer[i] = 0;
        }
        bool is_snake;
        do
        {
            is_snake = false;
            computer[0] = (unsigned char)(rand() % 256);
            computer_x = computer[0] >> 4;
            computer_y = computer[0] &0x0F;

            for(int i = 0 ; i < *length ; i++)
            {
                if(computer[0] == snake[i])
                {
                    is_snake = true;
                }
            }
        }
        while(computer_x == 0 || computer_x == map_size - 1 || computer_y == 0 || computer_y == map_size - 1 || is_snake );

    }

    if(*length >= 50)
    {
        *win = true;
    }
}


void map_setting(const unsigned char *snake, const unsigned char *computer, const unsigned char *lazer,
                 unsigned char *food,
                 const unsigned char *length, const unsigned char *computer_length, const unsigned char *lazer_length,
                 unsigned char (*map)[map_size], int size)
{

    unsigned char x, y;
    for(int i = 0 ; i < size ; i++)
	{
		for(int j = 0 ; j < size ; j++)
		{
			if(i == 0 || i == size - 1 || j == 0 || j == size - 1)//��
			{
				map[i][j] = WALL;
			}
			else
			{
				map[i][j] = 0;
			}
		}
	}

	x = *food >> 4;
    y = *food & 0x0F;
    map[y][x] = FOOD;

	for(int i = 0 ; i < *lazer_length ; i++)//�D
	{
		x = lazer[i] >> 4;
		y = lazer[i] &0x0F;
        if(lazer[i] > 0)
		{
			map[y][x] = LAZER;
		}
	}

	for(int i = 0 ; i < *length ; i++)//�D
	{
		x = snake[i] >> 4;
		y = snake[i] &0x0F;
        if(snake[i] > 0)
		{
			map[y][x] = SNAKE;
		}
	}
	for(int i = 0 ; i < *computer_length ; i++)//�D
	{
		x = computer[i] >> 4;
		y = computer[i] &0x0F;
        if(computer[i] > 0)
		{
			map[y][x] = COMPUTER;
		}
	}
}





void move_all(int direct, int *move, unsigned char *food, unsigned char *head_x, unsigned char *head_y,//fx, fy = food x, y�y�� //x, y �D�y��
                unsigned char *snake, unsigned char *computer, unsigned char *lazer, int *lazer_time, unsigned char *length,
                unsigned char *computer_length,  unsigned char *lazer_length, unsigned char (*map)[map_size], int size, bool *win, bool *lose)
{
	unsigned char fx, fy;//fx, fy = food x, y�y�� //x, y �D�y��
    fx = *food >> 4;//�Q�ΤG�i�� �k��4��p��x��
	fy = *food & 0x0F;//�Q��&�B��ŭp��y�ȡ]�Q���i�� 0x0F = �G�i�� 0000 1111�^

    move_lazer(snake, lazer, lazer_time, length, computer_length, lazer_length, map, map_size);
    move_snake(direct, food, head_x, head_y, fx, fy, snake, computer, length, computer_length, map, map_size);
    move_computer(move, food, fx, fy, snake, computer, length, computer_length, map, map_size);
    hit_the_snake_or_lazer(snake, computer, length, computer_length, map, map_size, win, lose);
	map_setting(snake, computer, lazer, food, length, computer_length, lazer_length, map, map_size);

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


void print_game_over(int size)
{
    int spiral_R[map_size][map_size], spiral_G[map_size][map_size];
    int mid = size / 2;
    int row = 0, column = 0;
    int R = 255, G = 255, B = 0;//�}�l�I
    spiral_R[mid][mid] = R;
    spiral_G[mid][mid] = G;

    for(int i = 0; i < size; i += 2)
    {
        row = mid - i / 2;//��_�I
        column = mid + i / 2;//��_�I

        //row����
        for(int first = 0; first < i; first++)
        {
            column -= 1;
            R -= 1;
            spiral_R[row][column] = R;
            G-= 1;
            spiral_G[row][column] = G;

        }

        //column����
        for(int second = 0; second < i; second++)
        {
            row += 1;
            R -= 1;
            spiral_R[row][column] = R;
            G-= 1;
            spiral_G[row][column] = G;
        }

        //row����
        for(int third = 0 ; third < i; third++)
        {
            column += 1;
            R -= 1;
            spiral_R[row][column] = R;
            G-= 1;
            spiral_G[row][column] = G;

        }

        //column����
        for(int forth = 0; forth < i; forth++)
        {
            row -= 1;
            R -= 1;
            spiral_R[row][column] = R;
            G-= 1;
            spiral_G[row][column] = G;

        }

    }







    for(int i = 0 ; i < size ; i++)
    {
        for(int j = 0 ; j < size ; j++)
        {
            printf("\033[48;2;%d;%d;0m  \033[0m", spiral_R[i][j], spiral_G[i][j]);
        }
        printf("\n");
    }

    printf("\n");
    printf("Game over! You lose!\n");
    printf("Press Enter to exit...\n");

}
