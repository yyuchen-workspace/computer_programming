
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main()
{
    char encrypted[100] = {};
    while ((scanf("%s", encrypted) != EOF))
    {
        int cnt_e[26] = {}; // 記錄加密消息中每個字母的頻率
        int length_e = strlen(encrypted);
        int repeat_e[length_e + 1]; // 記錄每個頻率出現的次數
        memset(repeat_e, 0, sizeof(repeat_e));

        for (int i = 0; i < length_e; i++)
        {
            cnt_e[encrypted[i] - 'A'] += 1; // 使用 'A' 而不是 'a'
        }
        for (int i = 0; i < 26; i++)
        {
            if (cnt_e[i] > 0) // 確保頻率有效
            {
                repeat_e[cnt_e[i]] += 1;
            }
        }

        char original[100] = {};
        scanf("%s", original);
        int length_o = strlen(original);
        int cnt_o[26] = {}; // 記錄原始消息中每個字母的頻率
        int repeat_o[length_o + 1]; // 記錄每個頻率出現的次數
        memset(repeat_o, 0, sizeof(repeat_o));

        for (int i = 0; i < length_o; i++)
        {
            cnt_o[original[i] - 'A'] += 1;
        }
        for (int i = 0; i < 26; i++)
        {
            if (cnt_o[i] > 0) // 確保頻率有效
            {
                repeat_o[cnt_o[i]] += 1;
            }
        }

        // 比較兩個頻率分佈是否相等
        bool repeated = true;
        for (int i = 0; i <= length_e && repeated; i++) // 比較範圍應為 0 ~ length_e
        {
            if (repeat_e[i] != repeat_o[i])
            {
                repeated = false;
            }
        }

        if (repeated)
        {
            printf("YES\n");
        }
        else
        {
            printf("NO\n");
        }
    }
    return 0;
}
