#include<stdio.h>
#include<stdint.h>
#include<stdbool.h>
int main()
{
    int32_t Z, I, M, L, case_ = 1;
    int32_t appeared[10000] = {0};//�x�s�w�X�{���Ʀr

    scanf("%d%d%d%d", &Z, &I, &M, &L);

    while(Z != 0 || I != 0 || M != 0 || L != 0)
    {
        int32_t times = 0;//�p��B�榸��
        int32_t repeat = 0;//���ƪ�����
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
            //����:���S����n���g�k�A�]���p�Gend = true���ɭԷ|�h��@���A���O�į�?��if(!end)��35~37��]�_�ӷ|���|����n
            times += 1;
            L = (Z * L + I) % M;
            appeared[times] = L;

        }


        printf("Case %d: %d\n", case_, repeat);
        case_ += 1;
        scanf("%d%d%d%d", &Z, &I, &M, &L);

    }
}
