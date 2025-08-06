#include "snake_function.h"

int main()
{
    unsigned char map[map_size][map_size] = {};
    unsigned char food;
    unsigned char snake[50] = {snake_initial};//ªì©l¤Æ³D®y¼Ð
    unsigned char computer[50] = {computer_initial};
    unsigned char lazer[lazer_size] = {};
    unsigned char length = 1;
    unsigned char computer_length = 1;
    unsigned char lazer_length = 3;


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

	int direct, move = 0;
	unsigned char head_x = 1, head_y = 1;
	bool win = false, lose = false, dead = false;
	int lazer_time = 5;
	srand((unsigned int)time(NULL));
    food = random_food(snake, computer, length, computer_length, map_size);
	while(1)
	{
		print_map(map, map_size, head_x, head_y, length);
		direct = get_direct(direct, &length);
		move_all(direct, &move, &food, &head_x, &head_y, snake, computer, lazer, &lazer_time, &length, &computer_length, &lazer_length, map, map_size, &win, &lose);
		dead = snake_hit_the_wall(snake);
		if(win)
		{
			print_game_win(map_size);
			getchar();
			break;
		}
		else if(lose || dead)
		{
            print_game_over(map_size);
			getchar();
			break;
		}

	}

	return 0;


}
