#include<stdio.h>


int min_pos(const int arr[], int sz)
{
    int min = 0;
    for(int i = 1 ; i < sz ; i++)
    {
        if(arr[i] < arr[min])
        {
            min = i;
        }
    }

    return min;
}

void swap(int *p, int *q)
{
    int tmp = *p;
    *p = *q;
    *q = tmp;
}
void sort(int arr[], int sz)
{
    for(int i = 0 ; i < sz ; i++)
    {
        int p = min_pos(&arr[i], sz-i);
        swap(&arr[i], &arr[p+i]);
    }
}


int main()
{
    int t = 0;
    int arr[10] = {};
    scanf("%d", &t);
    for(int i = 0 ; i < t ; i++)
    {
        scanf("%d", &arr[i]);
    }

    sort(arr, t);

    for(int i = 0 ; i < t ; i++)
    {
        printf("%d ", arr[i]);
    }


}
