#include<stdio.h>
int sum(int *arr, int size)
{
    int sum = 0;
    for(int i = 0 ; i < size ; i++)
    {
        sum += *(arr + i);
    }

    return sum;
}


float average(int *arr, int size)
{
    float avr = (float)sum(arr, size) / size;

    return avr;
}


void print(int *arr, int size)
{
    for(int i = 0 ; i < size ; i++)
    {
        printf("%d ", *(arr + i));
    }
    printf("\n");
}


void reset(int *arr, int size)
{
    for(int i = 0 ; i < size ; i++)
    {
        *(arr + i) = 0;
    }
}


int max(int *arr, int size)
{
    int max_value = *arr;
    for(int i = 0 ; i < size ; i++)
    {
        if(*(arr + i) > max_value)
        {
            max_value = *(arr + i);
        }
    }

    return max_value;
}


int max_pos(int *arr, int size)
{
    int max_index = 0;
    int max_value = max(arr, size);
    for(int i = 0 ; i < size ; i++)
    {
        if(max_value == *(arr + i))
        {
            max_index = i;
            break;
        }
    }

    return max_index;

}
