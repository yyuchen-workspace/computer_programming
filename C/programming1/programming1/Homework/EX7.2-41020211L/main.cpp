#include "numeric.h"

constexpr int size_of_array = 5;
int main()
{
    int arr[size_of_array] = {0};
    for(int i = 0 ; i < size_of_array ; i++)
    {
        scanf("%d", &arr[i]);
    }
    int sum_ = sum(arr, size_of_array);//returning the sum of all elements
    float average_ = average(arr, size_of_array);//returning the average (double) of all elements
    print(arr, size_of_array);//printing all elements in a single line
    reset(arr, size_of_array);//resetting all elements to zero
    int max_value = max(arr, size_of_array);//returning the maximum value
    max_pos(arr, size_of_array);//returning the index of the first found maximum element
}
