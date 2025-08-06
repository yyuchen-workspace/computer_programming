#include<stdio.h>
constexpr int max = 5;
int main()
{
    int function, x, y;
    int arr1[max][max] = {0}, arr2[max][max] = {0};
    printf("(1) Addition\n" "(2) Multiplication\n" "(3) Exit\n\n");
    printf("Please input the function...>");
    scanf("%d", &function);
    if(function == 3)
    {
        printf("Exit");
        return 0;
    }
    printf("Please specify the dimension x and y (max. 5)...>");
    scanf("%d%d", &x, &y);
    printf("Please input the first matrix:\n");
    for(int i = 0 ; i < x ; i++)//輸入(2,3)矩陣
    {
        for(int j = 0 ; j < y ; j++)
        {
            scanf("%d", &arr1[i][j]);
        }
    }

    printf("Please input the second matrix:\n");

    int answer[max][max] = {0};
    if(function == 2)
    {
        for(int i = 0 ; i < y ; i++)//輸入(3,2)矩陣
        {
            for(int j = 0 ; j < x ; j++)
            {
                scanf("%d", &arr2[i][j]);
            }
        }

        for(int i = 0 ; i < x ; i++)//計算相乘
        {
            for(int j = 0 ; j < x ; j++)
            {
                for(int k = 0 ; k < y ; k++)
                {
                        answer[i][j] += arr1[i][k] * arr2[k][j];
                }

            }
        }

        printf("The result of multiplication is:\n");
        for(int i = 0 ; i < x ; i++)
        {
            for(int j = 0 ; j < x ; j++)
            {
                printf("%d ", answer[i][j]);
            }
            printf("\n");
        }
 
    }

    else if(function == 1){
        for(int i = 0 ; i < x ; i++)//輸入(2,3)矩陣
        {
            for(int j = 0 ; j < y ; j++)
            {
                scanf("%d", &arr2[i][j]);
            }
        }

        for(int i = 0 ; i < x ; i++)//計算相加
        {
            for(int j = 0 ; j < y ; j++)
            {
                answer[i][j] = arr1[i][j] + arr2[i][j];
            }
        }

        printf("The result of Addition is:\n");
        for(int i = 0 ; i < x ; i++)
        {
            for(int j = 0 ; j < y ; j++)
            {
                printf("%d ", answer[i][j]);
            }
            printf("\n");
        }
    }
    return 0;
}
