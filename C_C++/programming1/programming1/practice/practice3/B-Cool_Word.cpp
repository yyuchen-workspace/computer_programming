#include <stdio.h>
#include <string.h>
#include <stdbool.h>
int main()
{
    int n = 0, testcase = 1;
    while (scanf("%d", &n)==1)
    {
        int ans = 0;
        for (int t=1; t<=n; t+=1)
        {
            bool repeated = false;
            char str[31] = {};
            scanf("%30s", str);
            if(strlen(str) < 2)
            {
                continue;
            }
            else
            {
                int cnt[26] = {};
                for (int i=0, sz=strlen(str); i<sz; i+=1)
                {
                    cnt[str[i]-'a'] += 1;
                }

                bool used[31] = {};
                for (int i = 0; i < 26 && !repeated; i += 1)
                {
                    if (cnt[i] > 0)
                    {
                        if (used[cnt[i]])
                        {
                            repeated = true; // 發現重複的頻率
                        }
                        else
                        {
                            used[cnt[i]] = true; // 標記該頻率已被使用
                        }
                    }
                }
                if(!repeated)
                {
                    ans+=1;
                }
            }


        }
    printf("Case %d: %d\n", testcase, ans);
    testcase += 1;
    }
}
