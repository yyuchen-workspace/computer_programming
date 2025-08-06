#include<stdio.h>
int main()
{
    int H1, M1, H2, M2;
    scanf("%d %d %d %d", &H1, &M1, &H2, &M2);
    while(H1 != 0 || M1 != 0 || H2 != 0 || M2 != 0)
        {
            int T1 = H1 * 60 + M1;
            int T2 = H2 * 60 + M2;
            int T_all = T2 - T1;
            if(T_all < 0)
            {
                T_all += 1440 ;
            }
            printf("%d\n", T_all);
            scanf("%d %d %d %d", &H1, &M1, &H2, &M2);
        }
    return 0;
}
