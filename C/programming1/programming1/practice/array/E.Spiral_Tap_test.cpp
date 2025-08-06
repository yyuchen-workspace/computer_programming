#include<stdio.h>
#include<stdint.h>
#include<math.h>
constexpr int32_t Max = 100000;

int main()
{
    int32_t SZ, P;
    scanf("%d%d", &SZ, &P);
    while(SZ != 0&& P != 0)
    {
        int32_t circle = 0, last_circle = 0, max_circle = 0;
        int32_t step = 0, line = 0, line_step = 0;
        int32_t bordon = 0, row = 0, column = 0, row_start = 0, column_start = 0;
        int32_t top = 0, left = 1, bottom = 2, right = 3;
        max_circle = (SZ + 1) / 2;//最外圈在第幾圈，1是第一圈, i = 3是第二圈...
        if(P == 1)
        {
            row = (SZ + 1) / 2;
            column = (SZ + 1) / 2;
        }
        else
        {
            for(int i = 1 ; i < Max ; i+=2)
            {
                if(P <= i * i)
                {
                    bordon = i;//行列最大值
                    circle = (i + 1) / 2;//在第幾圈，i = 1是第一圈, i = 3是第二圈...

                    row_start = i + (max_circle - circle);//目標數字的圈+(最外圈-目的圈數)，得出起點在第幾行...
                    column_start = i + (max_circle - circle);
                    last_circle = (i - 2) * (i - 2);
                    break;
                }
            }
            line = 2 * (circle - 1);//一行幾格
            step = P - last_circle;//在該圈走幾步
            line_step = (step - 1) % line + 1;//在該行走幾步,起點在該圈終點;
            int32_t objective_line = (step - 1) / line;
            if(objective_line == top)
            {
                row = row_start;
                column = column_start - line_step;
            }
            else if(objective_line == left)
            {
                row = row_start - line_step;
                column = column_start - line;
            }
            else if(objective_line == bottom)
            {
                row = row_start - line;
                column = column_start - line + line_step;
            }
            else if(objective_line == right)
            {
                row = row_start - line + line_step;
                column = column_start;
            }
        }
        printf("Line = %d, column = %d.\n", row, column);

        scanf("%d%d", &SZ, &P);
    }
}
