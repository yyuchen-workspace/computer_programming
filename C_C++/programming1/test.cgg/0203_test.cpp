#include<stdio.h>
#include<string.h>
#include<stdint.h>

int32_t num;//將輸入的數字儲存
int times = 0;
char result1;
char result2;
char result3;
char arr[7][2] = {"0", "1", "2", "3", "4", "5", "6"}; //S1 ~ S6

int main()
{
    printf("Please enter an integer");
    scanf("%d", num);
    while(num != 0)
    {
        while_loop();
    }
    printf("Possible States : %d, %d", result1, result2);
} 




void while_loop()
{

    while(num != 0)//S0變化
    {   
        if(num % 2 != 0)//odd
        {
            result1 = arr[1][0];//to S1
            result2 = arr[2][0];//to S2
            while(num != 0)
            {           
                printf("Please enter an integer");
                scanf("%d", num);
                if( num % 2 != 0)//S2 odd變化
                {
                    result1 = arr[2][0]; //S3
                    while(num != 0)
                    {
                        printf("Please enter an integer");
                        scanf("%d", num);
                        if(num % 2 != 0) //S3odd變化
                        {
                            result1 = arr[4][0];
                        }
                        else
                        {
                            return;
                        }
                    }
                } 
                else//S1 S2 even變化
                {
                    result1 = arr[3][0]; //S4
                    result2 = arr[4][0]; //S5
                    printf("Please enter an integer");
                    scanf("%d", num);
                    while (num != 0)
                    {
                        if(num % 2 != 0)
                        {
                            result1 = arr[4][0]; //S5
                            result2 = arr[5][0]; //S6
                            printf("Please enter an integer");
                            scanf("%d", num);
                            while                      
                        }
                        else
                        {
                            
                        }
                    }
                }

               
            } 
        
        }
        else
        {
            result1 = arr[2][0];//to S3
            while(num != 0)
            {
                printf("Please enter an integer");
                scanf("%d", num);    
                //////////          
            }
        }
        
        

    }
}


