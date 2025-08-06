#include<stdio.h>
int main()
{
    int times;
    scanf("%d", &times);

    for(int i = 0 ; i < times ; i++)
    {
        if(i > 0)
        {
            printf("\n");
        }
        int Amplitude = 0;
        int Frequency = 0;
        scanf("%d %d", &Amplitude, &Frequency);

        for(int j = 0 ; j < Frequency ; j++)
        {

            for(int k = 1 ; k <= Amplitude ; k++)
            {
                for(int L = 0 ; L < k ; L++)
                {
                   printf("%d", k);
                }

                printf("\n");
            }
            for(int k = Amplitude - 1 ; k > 0 ; k--)
            {
                for(int L = 0 ; L < k ; L++)
                {
                   printf("%d", k );
                }

                printf("\n");

            }
            if(j < Frequency - 1)
            {
                printf("\n");
            }

        }
    }

    return 0;
}
