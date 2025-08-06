#include<stdio.h>

int main()
{
    int n;
    scanf("%d", &n);

    int arr[100];
    for(int i = 0 ; i < n ;i++)
    {
        scanf("%d", &arr[i]);
    }

    int count = 0;
    for(int i = 0 ; i < n - 2; i++)
    {
        for(int j = i+1 ; j < n - 1; j++)
        {
            for(int k = j+1 ; k < n ; k++)
            {
                if(arr[i] > arr[j] && arr[j] < arr[k])
                {
                    count+=1;
                }
            }
        }
    }

    printf("%d\n", count);
}
