#include<stdio.h>


int * min_element(int data[], int size)
{
    int *min = data;
    for(int i = 0 ; i < size ; i++)
    {
        if(data[i] < *min)
        {
            min = &data[i];
        }
    }
    return min;
}

void min_max_element(int **min, int **max, int arr[], int size)
{
    *min = arr, *max = arr;
    for(int i = 1 ; i < size ; i++)
    {
        if(arr[i] < **min)
        {
            *min = &arr[i];
        }

        if(arr[i] > **max)
        {
            *max = &arr[i];
        }
    }
}

int main()
{
    constexpr int DataSize = 5;
    int arr[DataSize] = {};

    for (int i=0; i<DataSize; i+=1)
    {
        scanf("%d", &arr[i]);
    }

    printf("min: %d\n", *min_element(arr, DataSize));

    int *min = nullptr, *max = nullptr;
    min_max_element(&min, &max, arr, DataSize);
    printf("min: %d, max: %d\n", *min, *max);

    *min = 0;
    *max = 100;

    for (int i=0; i<DataSize; i+=1)
    {
        printf("%d ", arr[i]);
    }
}

