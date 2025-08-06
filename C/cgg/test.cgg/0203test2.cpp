#include<stdio.h>
#include<string.h>
int main()
{
    int num = 0;
    char result[7][3] = {0};
    
    char S[][3] = {"S0", "S1", "S2", "S3", "S4", "S5", "S6"};
    printf("Please enter an integer : ");
    scanf("%d", &num);
    if(num == 0)
    {
        printf("Possible States : %s", S[0]);
    }
    if(num % 2 != 0) //odd
    {
        strcpy (result[0], S[1]);
        strcpy (result[0], S[2]);
    }   
    else
    {
        strcpy(result[0], S[3]);
    }

    while(num != 0)
    {
        printf("Please enter an integer : ");
        scanf("%d", &num);
        
        if(num == 0)
        {
            printf("Possible States : %s", result[0]);
        
            if(result[1] != 0 && result[1] != result[0])
            {
                printf(", %s", result[1]);
            }
            
            if(result[2] != 0 && result[2] != result[1] && result[2] != result[0])
            {
                printf(", %s", result[2]);
            }
            
            if(result[3] != 0 && result[3] != result[2] && result[3] != result[1] && result[3] != result[0])
            {
                printf(", %s", result[3]);
            }
            
            if(result[4] != 0 && result[4] != result[3] && result[4] != result[2] && result[4] != result[1] && result[4] != result[0])
            {
                printf(", %s", result[4]);
            }

            if(result[5] != 0 && result[5] != result[4] && result[5] != result[3] && result[5] != result[2] && result[5] != result[1] && result[5] != result[0])
            {
                printf(", %s", result[5]);
            }

             if(result[6] != 0 && result[6] != result[5] && result[6] != result[4] && result[6] != result[3] && result[6] != result[2] && result[6] != result[1] && result[6] != result[0])
            {
                printf(", %s", result[6]);
            }
        }
        
        
        for(int i = 0; i < 7 ; i++)
        {
            switch (result[i][2])
            {
                case 0:
                    if(num % 2 == 0)
                    {
                        strcpy(result[i], result[0]);
                    }
                    
                    break;//想要坐樹狀
                case 1:
                    strcpy(result[i], result[1]);
                    break;
                case 2:
                    strcpy(result[i], result[2]);
                    break;
                case 3:
                    strcpy(result[i], result[3]);
                    break;
                case 4:
                    strcpy(result[i], result[4]);
                    break;
                case 5:
                    strcpy(result[i], result[5]);
                    break;
                case 6:
                    strcpy(result[i], result[6]);
                    break;
            }

        }






    }
}