#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <windows.h>
#include <time.h>
#include <stdbool.h>

constexpr int MAP_SIZE = 17;
constexpr int MAX_LENGTH = 50;

constexpr int SNAKE_START = 77;
constexpr int COMPUTER_START = 55;

constexpr int UP = 72;
constexpr int DOWN = 80;
constexpr int LEFT = 75;
constexpr int RIGHT = 77;

constexpr int LAZER = 5;
constexpr int COMPUTER = 4;
constexpr int SNAKE = 3;
constexpr int FOOD = 2;
constexpr int WALL = 1;

void print_map(const unsigned char map[MAP_SIZE][MAP_SIZE], unsigned char head_x, unsigned char head_y)
{
    for (int i = 0; i < MAP_SIZE; i++)
    {
        for (int j = 0; j < MAP_SIZE; j++)
        {
            switch (map[i][j])
            {
                case WALL:
                    printf("\033[48;2;255;199;6m  \033[0m"); // Orange wall
                    break;
                case LAZER:
                    printf("\033[48;2;255;255;0m  \033[0m"); // Yellow laser
                    break;
                case COMPUTER:
                    printf("\033[48;2;255;0;255m  \033[0m"); // pink computer snake
                    break;
                case SNAKE:
                    if (i == head_y && j == head_x)
                    {
                        printf("\033[48;2;0;125;255m  \033[0m"); // blue snake head
                    }
                    else
                    {
                        printf("\033[48;2;0;255;255m  \033[0m"); // blue snake body
                    }
                    break;
                case FOOD:
                    printf("\033[48;2;255;0;0m  \033[0m"); // Red food
                    break;
                default:
                    printf("  ");
            }
        }
        printf("\n");
    }
    Sleep(500);
    system("cls");
}

int get_direction(int current_direction, unsigned char snake_length)//讀取輸入
{
    int new_direction = current_direction;
    if (_kbhit())
    {
        getch();
        new_direction = getch();
    }

    if (snake_length > 1 && abs(new_direction - current_direction) == 8)
    {
        return current_direction;
    }

    return new_direction;
}

unsigned char random_food(unsigned char* snake, unsigned char* computer, unsigned char snake_length, unsigned char computer_length)
{
    unsigned char food, fx, fy;
    bool overlaps;

    do {
        overlaps = false;
        food = (unsigned char)(rand() % 256);
        fx = food >> 4;
        fy = food & 0x0F;

        for (int i = 0; i < snake_length; i++)
        {
            if (food == snake[i])
            {
                overlaps = true;
                break;
            }
        }

        for (int i = 0; i < computer_length; i++)
        {
            if (food == computer[i])
            {
                overlaps = true;
                break;
            }
        }

    }while (fx == 0 || fx == MAP_SIZE - 1 || fy == 0 || fy == MAP_SIZE - 1 || overlaps);

    return food;
}

int ensure_no_wall_collision(int move, unsigned char x, unsigned char y)
{
    static const int dx[] = {0, 0, -1, 1};
    static const int dy[] = {-1, 1, 0, 0};

    int new_x = x + dx[move];
    int new_y = y + dy[move];

    while (new_x <= 0 || new_x >= MAP_SIZE - 1 || new_y <= 0 || new_y >= MAP_SIZE - 1)
    {
        move = rand() % 4;
        new_x = x + dx[move];
        new_y = y + dy[move];
    }

    return move;
}

int choose_move_toward_food(unsigned char x, unsigned char y, unsigned char fx, unsigned char fy)
{
    if (abs(x - fx) > abs(y - fy))
    {
        return (x > fx) ? LEFT : RIGHT;
    }
    else
    {
        return (y > fy) ? UP : DOWN;
    }
}

void move_entity(unsigned char* entity, int move, unsigned char& x, unsigned char& y)
{
    switch (move)
    {
        case UP:    y--; break;
        case DOWN:  y++; break;
        case LEFT:  x--; break;
        case RIGHT: x++; break;
    }
    entity[0] = (x << 4) | y;
}

void update_map(unsigned char map[MAP_SIZE][MAP_SIZE], unsigned char* snake, unsigned char* computer, unsigned char fx,
                 unsigned char fy, unsigned char snake_length, unsigned char computer_length)
{
    for (int i = 0; i < MAP_SIZE; i++)
    {
        for (int j = 0; j < MAP_SIZE; j++)
        {
            if (i == 0 || i == MAP_SIZE - 1 || j == 0 || j == MAP_SIZE - 1)
            {
                map[i][j] = WALL;
            }
            else
            {
                map[i][j] = 0;
            }
        }
    }

    map[fy][fx] = FOOD;

    for (int i = 0; i < snake_length; i++)
    {
        if (snake[i])
        {
            unsigned char x = snake[i] >> 4;
            unsigned char y = snake[i] & 0x0F;
            map[y][x] = SNAKE;
        }
    }

    for (int i = 0; i < computer_length; i++)
    {
        if (computer[i])
        {
            unsigned char x = computer[i] >> 4;
            unsigned char y = computer[i] & 0x0F;
            map[y][x] = COMPUTER;
        }
    }
}

bool check_collision(unsigned char* snake, unsigned char* computer, unsigned char snake_length, unsigned char computer_length, bool& win)
{
    unsigned char head_x = snake[0] >> 4;
    unsigned char head_y = snake[0] & 0x0F;

    for (int i = 1; i < computer_length; i++)
    {
        if (snake[0] == computer[i])
        {
            return true; // Lose condition
        }
    }

    if (head_x == (computer[0] >> 4) && head_y == (computer[0] & 0x0F))
    {
        return true; // Lose condition
    }

    if (snake[0] == computer[0])
    {
        win = true;
    }

    return false;
}

int main()
{
    unsigned char map[MAP_SIZE][MAP_SIZE] = {0};
    unsigned char snake[MAX_LENGTH] = {SNAKE_START};
    unsigned char computer[MAX_LENGTH] = {COMPUTER_START};
    unsigned char food;
    unsigned char snake_length = 1;
    unsigned char computer_length = 1;

    unsigned char head_x = SNAKE_START >> 4;
    unsigned char head_y = SNAKE_START & 0x0F;

    int direction = RIGHT;
    bool win = false, lose = false;

    srand((unsigned int)time(NULL));
    food = random_food(snake, computer, snake_length, computer_length);

    while (!win && !lose)
    {
        print_map(map, head_x, head_y);
        direction = get_direction(direction, snake_length);//讀取輸入

        move_entity(snake, direction, head_x, head_y);
        lose = check_collision(snake, computer, snake_length, computer_length, win);

        if (!win && !lose)
        {
            unsigned char food_x = food >> 4;
            unsigned char food_y = food & 0x0F;
            update_map(map, snake, computer, food_x, food_y, snake_length, computer_length);
        }
    }

    printf(win ? "You Win!\n" : "Game Over!\n");
    return 0;
}
