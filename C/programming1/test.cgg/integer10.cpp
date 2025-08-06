//隨機輸入10個數字並先依照偶數在前奇數在後排列，並再依照由小到大排列
#include<stdio.h>
#include<stdint.h>
#include<stdlib.h>
#include<time.h>
#define times 10
int main()
{
    srand(time(0));
    int array[times];
    int even[times];
    int odd[times];
    for(int i = 0; i < times; i++ ){
        array[i] = rand()%999;
    }
    for(int i = 0 ; i < times ; i++){
        printf("%d\n", array[i]);
    }
    int even_num = 0;
    int odd_num = 0;
    for (int i = 0; i < times; i++){
            if(array[i] % 2 == 0){
                even[even_num] = array[i];
                even_num++;               
            }
            else{
                odd[odd_num] = array[i];
                odd_num++;
            }
        }
    for (int i = 0; i < even_num; i++){
        for(int j = i + 1; j < even_num; j++){
            if(even[i] > even[j]){
                int32_t tmp = even[i];
                even[i] = even[j];
                even[j] = tmp;
            }
        }
    } 
    for (int i = 0; i < odd_num; i++){
        for(int j = i + 1; j < odd_num; j++){
            if(odd[i] > odd[j]){
                int32_t tmp = odd[i];
                odd[i] = odd[j];
                odd[j] = tmp;
            }
        }
    }
    for (int i = 0 ; i < even_num ; i++){
        printf("%d ", even[i]);
    }

    for(int i = 0; i < odd_num ; i++){
        printf("%d ", odd[i]);
    }
    return 0;
}