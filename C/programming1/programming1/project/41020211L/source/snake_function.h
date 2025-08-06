#ifndef SNAKE_FUNCTION_INCLUDED
#define  SNAKE_FUNCTION_INCLUDED

#include<stdio.h>
#include<conio.h>
#include<stdlib.h>
#include<windows.h>
#include<time.h>
#include<stdbool.h>
#include<stdint.h>


constexpr int map_size = 17;
constexpr int lazer_size = 6;

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

void print_map(const unsigned char (*map)[map_size], int size, unsigned char head_x, unsigned char head_y, unsigned char length);


int get_direct(int old_direct, unsigned char *length);


unsigned char random_food(const unsigned char *snake, const unsigned char *computer, const unsigned char length, const unsigned char computer_length, int size);


void if_hit_the_wall(int *move, const unsigned char computer_x, const unsigned char computer_y, int size);


int choose_move_toward_food(const unsigned char computer_x, const unsigned char computer_y, const unsigned char fx, const unsigned char fy);


void move_computer(int *move, unsigned char *food, unsigned char fx, unsigned char fy,
                   const unsigned char *snake, unsigned char *computer, const unsigned char *length,
                   unsigned char *computer_length, unsigned char (*map)[map_size], int size);


void move_lazer(const unsigned char *snake, unsigned char *lazer, int *lazer_time,
                const unsigned char *length, const unsigned char *computer_length, unsigned char *lazer_length,
                 unsigned char (*map)[map_size], int size);



void move_snake(int direct, unsigned char *food, unsigned char *head_x, unsigned char *head_y,
                unsigned char fx, unsigned char fy,
                unsigned char *snake, unsigned char *computer, unsigned char *length,
                unsigned char *computer_length, unsigned char (*map)[map_size], int size);



void hit_the_snake_or_lazer(unsigned char *snake, unsigned char *computer, unsigned char *length,
                            unsigned char *computer_length,unsigned char (*map)[map_size], int size, bool *win, bool *lose);



void map_setting(const unsigned char *snake, const unsigned char *computer, const unsigned char *lazer,
                 unsigned char *food,
                 const unsigned char *length, const unsigned char *computer_length, const unsigned char *lazer_length,
                unsigned char (*map)[map_size], int size);



void move_all(int direct, int *move, unsigned char *food, unsigned char *head_x, unsigned char *head_y,//fx, fy = food x, y®y¼Ð //x, y ³D®y¼Ð
                unsigned char *snake, unsigned char *computer, unsigned char *lazer, int *lazer_time,
                unsigned char *length, unsigned char *computer_length,  unsigned char *lazer_length,
                unsigned char (*map)[map_size], int size, bool *win, bool *lose);



bool snake_hit_the_wall(unsigned char *snake);


void print_game_win(int size);


void print_game_over(int size);


#endif // SNAKE_FUNCTION_INCLUDED
