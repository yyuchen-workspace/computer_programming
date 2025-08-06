#include<stdio.h>

int main()
{
    int combo;
    scanf("%d", &combo);
    for(int i = combo ; i > 0 ; i--)
    {
        for(int j = 1 ; j < i ; j++)
        {
            printf(" ");
        }
        printf("%d combo hits!\n", i);
    }

    return 0;
}
