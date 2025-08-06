#include<stdio.h>
int main(){
    int score;
    int times;
    int Max = 0;
    int min = 100;
    double passrate;
    double total;
    double avg;
    printf("Please input a score (-1 to end)...>");
    scanf("%d", &score);

    while(score != -1){
        total+=score;
        times++;
        if(score >= Max){
            Max = score;
        }
        if(score <= min){
            min = score;
        }
        if(score >= 60){
            passrate += 1.0;
        }
        printf("Please input a score (-1 to end)...>");
        scanf("%d", &score);
    }
    printf("\n", "Analysis\n", "---------------------");
    if(total == 0){
        printf("no score is input or all score is zero\n");
    }
    else{
        avg = total/times;
        printf("Max: %d\n", Max);
        printf("min: %d\n", min);
        printf("Avg: %.2f\n", avg);
        printf("Pass rate: %.0f%%", passrate/times*100);

    }


}
