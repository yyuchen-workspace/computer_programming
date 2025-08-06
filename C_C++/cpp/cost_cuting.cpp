#include<stdio.h>
int main()
{
    int num;
    int salary[3];
    scanf("%d", &num);
    int mid[num];
    if(num > 20)
    {
        return 0;
    }
    for(int i = 0; i < num ; i++)//執行num次
    {
        for(int j = 0 ; j < 3 ; j++)//輸入三個數字
        {
            scanf("%d", &salary[j]);
        }
        for(int a = 0 ; a < 3 ; a++)//排序由小到大
        {
            for(int b = a + 1; b < 3 ; b++)
            {
                if(salary[a] > salary[b])
                {
                    int tmp = salary[a];
                    salary[a] = salary[b];
                    salary[b] = tmp; 
                }
            }
        }
        mid[i] = salary[1];
        
    }
    
    for(int i = 0 ; i < num ; i++)
    {
        printf("Case %d: %d\n", i+1, mid[i]);
    }




}