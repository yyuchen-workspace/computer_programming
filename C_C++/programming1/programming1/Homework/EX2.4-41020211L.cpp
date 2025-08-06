#include<stdio.h>
int main()
{
    int a;
    int cal;
    int b;
    printf("Advanced calculator\n");
    printf("Input example: 100 1 30 means 100 + 30\n");
    printf("For the second integer,1,2,3,4 and 5 refer to +,-,*,/,and%,respectively.\n");    
    
    while(true)
    {
        printf("Your input...>");
        scanf("%d%d%d", &a, &cal, &b);
        printf("\n");

        switch(cal)
        {
            case 1:   
            printf("%d+%d=%d.", a, b, a+b); 
            break;
        
            case 2:
            printf("%d-%d=%d.", a, b, a-b);
            break;

            case 3:
            printf("%d*%d=%d.", a, b, a*b);
            break;

            case 4:
            printf("%d/%d=%d.", a, b, a+b);
            break;

            case 5:
            printf("%d%%%d=%d.", a, b, a%b);
            break;

            case 0:
            if(a == 0 && b == 0)
            {
                printf("Thanks for using the calculator. Bye!\n");
                break;
            }
            else
            {
                printf("Input 0 0 0 to end the program.\n");
            }

            default: 
            printf("Invalid operrator! The second integer should be in {0,1,2,3,4,5}.");
        }
    }
}



