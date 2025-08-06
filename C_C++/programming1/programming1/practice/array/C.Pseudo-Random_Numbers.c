#include<stdio.h>
#include<stdint.h>
#include<stdbool.h>
int main()
{
    int32_t Z, I, M, L, case_ = 1;
    int32_t appeared[10000] = {0};//儲存已出現的數字

    scanf("%d%d%d%d", &Z, &I, &M, &L);

    while(Z != 0 || I != 0 || M != 0 || L != 0)
    {
        int32_t times = 0;//計算運行次數
        int32_t repeat = 0;//重複的長度
        bool end = false;
        appeared[0] = L;

        while(!end)
        {
            for(int i = 0 ; i <  times ; i++)
            {
                if(times == 0)
                {
                    break;
                }
                if(L == appeared[i])
                {
                    repeat = times - i;
                    end = true;
                    break;
                }

            }
            //提問:有沒有更好的寫法，因為如果end = true的時候會多算一次，浪費效能?用if(!end)把35~37行包起來會不會比較好
            times += 1;
            L = (Z * L + I) % M;
            appeared[times] = L;

        }


        printf("Case %d: %d\n", case_, repeat);
        case_ += 1;
        scanf("%d%d%d%d", &Z, &I, &M, &L);

    }
}
