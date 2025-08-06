#include<stdio.h>
int main()
{
    int array[11]; 
    for(int i = 0 ; i < 11 ; i++)
    { 
        scanf("%u", &array[i]);
    }
    for(int i = 0 ; i < 11 ; i++)
    {
        for(int j = i ; j < 11 ; j++)
        {
            if(array[i] < array[j])
            {
                int temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }
    }
    printf("%d", array[5]);
}