#include<stdio.h>
int main()
{
    int a;
    int cal;
    int b;
    printf("Advanced calculator\n");
    printf("Input example: 100 1 30 means 100 + 30\n");
    printf("For the second integer,1,2,3,4, and 5 refer to +,-,*,/,and%,respectively.\n");
    printf("Your input...>");
    scanf("%d%d%d", &a, &cal, &b);
    printf("\n", "\n");


    if (b == 0 && (cal == 4 || cal == 5)){
            printf("the Divisor cannot be zero.\n");
            printf("Please input the second operand again...>");
            scanf("%d", &b);
            printf("\n", "\n");
            if(b == 0){
                printf("I have no more patience.\n");
                return 0;
            }
    }

    if(cal == 1){
        printf("%d+%d=%d.", a, b, a+b);
    }
    else if(cal == 2){
        printf("%d-%d=%d.", a, b, a-b);
    }
    else if(cal == 3){
        printf("%d*%d=%d.", a, b, a*b);
    }
    else if(cal == 4){
        printf("%d/%d=%d.", a, b, a/b);
    }
    else{
        printf("%d%%%d=%d.", a, b, a%b);
    }

    return 0 ;
}



