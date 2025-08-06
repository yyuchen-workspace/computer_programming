//骰骰子60000次，並計算出六種點數的個數
#include<stdio.h>
#include <stdlib.h>
#include <time.h>
#define size 60000

int main() {
    
    srand(time(0));
    int one = 0;
    int two = 0;
    int three = 0;
    int four = 0;
    int five = 0;
    int six = 0;
    int array[size];
    for(int i = 0; i < sizeof(array)/ sizeof(int); i++)
    {
        int dice = (rand() % 6) + 1;
        array[i] = dice;
        if (array[i] == 1)
        {
            one++;
        }
        array[i] = dice;
        if(array[i] == 2){
            two++;
        }
        array[i] = dice;
        if(array[i] == 3){
            three++;
        }
        array[i] = dice;
        if(array[i] == 4){
            four++;
        }
        array[i] = dice;
        if(array[i] == 5){
            five++;
        }
        array[i] = dice;
        if(array[i] == 6){
            six++;
        }

    }
    printf("number one : %d\n", one);
    printf("number two : %d\n", two);
    printf("number three : %d\n", three);
    printf("number four : %d\n", four);
    printf("number five : %d\n", five);
    printf("number six : %d\n", six);

    return 0;

   
}