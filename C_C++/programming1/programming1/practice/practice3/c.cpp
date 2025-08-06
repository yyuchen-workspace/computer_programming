#include<stdio.h>
#include<string.h>
#include<stdbool.h>

int main()
{
    char encrypting[101] = {};
    while(scanf("%s", encrypting) != EOF)
    {
        int enc_cln[26] = {};
        int enc_length = strlen(encrypting);
        int enc_repeated[enc_length+1] = {};

        for(int i = 0 ; i < enc_length ; i++)
        {
            enc_cln[encrypting[i] - 'A'] += 1;
        }
        for(int i = 0 ; i < 26 ; i++)
        {
            if(enc_cln[i] > 0)
            {
                enc_repeated[enc_cln[i]] += 1;
            }
        }


        char original[101] = {};
        scanf("%s", original);
        int ori_cln[26] = {};
        int ori_length = strlen(original);
        int ori_repeated[ori_length+1] = {};


        for(int i = 0 ; i < ori_length ; i++)
        {
            ori_cln[original[i] - 'A'] += 1;
        }
        for(int i = 0 ; i < 26 ; i++)
        {
            if(ori_cln[i] > 0)
            {
                ori_repeated[ori_cln[i]] += 1;
            }
        }


        bool not_repeated = true;
        for(int i = 0 ; i <= enc_length && not_repeated ; i++)
        {
            if(enc_repeated[i] != ori_repeated[i])
            {
                not_repeated = false;
            }
        }

        if(not_repeated)
        {
            printf("YES\n");
        }
        else
        {
            printf("NO\n");
        }





    }
}
