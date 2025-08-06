#include<stdio.h>
#include<stdbool.h>

int main()
{
    int a;
    int cal;
    int b;
    int end = false;
    printf("Advanced calculator\n");
    printf("Input example: 100 1 30 means 100 + 30\n");
    printf("For the second integer,1,2,3,4 and 5 refer to +,-,*,/,and%,respectively.\n");    
    
    while(!end)
    {
        printf("Your input...>");
        scanf("%d%d%d", &a, &cal, &b);
        printf("\n");

        

        switch(cal)
        {
            case 1:   
            printf("%d + %d = %d.\n", a, b, a+b); 
            printf("\n");
            break;
        
            case 2:
            printf("%d - %d = %d.\n", a, b, a-b);
            printf("\n");
            break;

            case 3:
            printf("%d * %d = %d.\n", a, b, a*b);
            printf("\n");
            break;

            case 4:
            while(b == 0)
            {
                printf("The divisor cannot be zero.\n");
                printf("Please input the second operand again…>");
                scanf("%d", &b);   
                printf("\n");
            }    
                printf("%d / %d = %d.\n", a, b, a / b);
                printf("\n");
                break;
            
            case 5:
            printf("%d %% %d = %d.\n", a, b, a%b);
            printf("\n");
            break;

            case 0:
            if(a == 0 && b == 0)
            {
                printf("Thanks for using the calculator. Bye!\n");
                end = true;
                break;
            }
            else
            {
                printf("Input 0 0 0 to end the program.\n");
                printf("\n");
                break;
            }

            default: 
            printf("Invalid operrator! The second integer should be in {1,2,3,4,5}.\n");
            printf("\n");
            break;
        }
    }
}



