#include<stdio.h>
#include<stdint.h>



int32_t return_end_num(int number[75], int32_t bingos[5][5], int32_t row[5], int32_t column[5],  int32_t diagonal[2])
{
    int end_num = 1;

    for(int j = 0 ; j < 75 ; j++)
    {
        for(int k = 0 ; k < 5 ; k++)
        {
            for(int l = 0 ; l < 5 ; l++)
            {
                if(number[j] == bingos[k][l])
                {
                    row[k] += 1;
                    column[l] += 1;
                    if(k == l)
                    {
                        diagonal[0] += 1;
                    }
                    if(k + l == 4)
                    {
                        diagonal[1] += 1;
                    }
                    if(row[k] == 5 || column[l] == 5 || diagonal[0] == 5 || diagonal[1] == 5)
                    {
                        return end_num;
                    }
                }




                }
            }
            end_num += 1;

    }
}

int main()
{
    int32_t games;
    scanf("%d", &games);
    for(int i = 0 ; i < games ; i++)
    {
        int32_t bingos[5][5] = {0};
        int32_t row[5] = {0};
        int32_t column[5] = {0};
        int32_t diagonal[2] = {0};
        int32_t number[75] = {0};
        int32_t is_bingo = 0;
        row[2] = 1;//free space
        column[2] = 1;//free space
        diagonal[0] = 1;//free space
        diagonal[1] = 1;//free space
        for(int j = 0 ; j < 5 ; j++)
        {
            for(int k = 0 ; k < 5 ; k++)
            {
                if(j == 2 && k == 2)
                {
                    bingos[j][k] = 0;
                }
                else
                {
                    scanf("%d", &bingos[j][k]);
                }
            }
        }

        for(int j = 0 ; j < 75 ; j++)
        {

            scanf("%d", &number[j]);
            while(number[j] < 1 || number[j] > 75)
            {
                scanf("%d", &number[j]);
            }
        }

        is_bingo = return_end_num(number, bingos, row, column, diagonal);
        printf("BINGO after %d numbers announced\n", is_bingo);
    }
}
