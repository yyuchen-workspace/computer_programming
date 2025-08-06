#include<stdio.h>

int hanoi(int n, int *count, char T1, char T2, char T3)
{
    if(n < 1) return 1;
    if(n == 1)
    {
        printf("%c 最上層盤子移到 %c木樁\n", T1, T3);
        (*count)++;
    }
    else
    {
        hanoi(n - 1, count, T1, T3, T2);
        printf("%c 最上層盤子移到 %c木樁\n", T1, T3);
        (*count)++;
        hanoi(n - 1, count, T2, T1, T3);
        (*count)++;
    }
    return 0;
}

int main()
{
    int n;
    int count;
    printf("請輸入盤子數量: ");
    scanf("%d", &n);
    int do_hanoi = hanoi(n, &count, 'A', 'B', 'C');
    printf("共移動了 %d 次\n", count);
    return 0;
}