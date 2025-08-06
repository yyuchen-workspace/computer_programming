#include<stdio.h>
#include<string.h>

int main()
{
    int n, cases = 1;
    while(scanf("%d", &n) == 1)
    {

        int cool_words = 0;
        for(int t = 0 ; t < n ; t++)
        {
            char letters[31] = {};
            int cln[26] = {};
            scanf("%s", letters);
            if(strlen(letters) < 2)
            {
                continue;
            }

            for(int i = 0, sz = strlen(letters) ; i < sz ; i++)
            {
                cln[letters[i] - 'a'] += 1;
            }

            bool is_used = false;
            bool used[31] = {};
            for(int i = 0 ; i < 26 && !is_used; i++)
            {
                if(cln[i] > 0)
                {
                    if(used[cln[i]])
                    {
                        is_used = true;
                        break;
                    }
                    else
                    {
                        used[cln[i]] = true;
                    }
                }
            }

                if(!is_used)
                {
                    cool_words+=1;
                }

        }

        printf("Case %d: %d\n", cases, cool_words);
        cases+=1;


    }
}
