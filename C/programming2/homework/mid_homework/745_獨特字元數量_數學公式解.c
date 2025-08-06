#include <stdio.h>
#include <string.h>

#define MAXN 50005

int main() {
    char s[MAXN];
    scanf("%s", s);
    int len = strlen(s);

    // 每個字元記錄出現位置（最多 26 個英文字母）
    int idx[26][MAXN];
    int count[26] = {0};

    // 把每個字母出現位置記錄下來
    for (int i = 0; i < len; ++i) {
        int c = s[i] - 'a';
        idx[c][count[c]++] = i;
    }

    long long ans = 0;

    for (int c = 0; c < 26; ++c) {
        for (int i = 0; i < count[c]; ++i) {
            int prev = (i == 0) ? -1 : idx[c][i - 1];
            int curr = idx[c][i];
            int next = (i == count[c] - 1) ? n : idx[c][i + 1];

            ans += (long long)(curr - prev) * (next - curr);
        }
    }

    printf("%lld\n", ans);
    return 0;
}



/*對每個字母的每一個出現位置 i，設：

prev 是它前一次出現的位置（沒有就為 -1）

next 是它下一次出現的位置（沒有就為字串長度 n）

那麼 這個位置的貢獻值為：(𝑖−prev)×(next−𝑖)

因為：

有 i - prev 種起點，讓這個字元是第一個（從 prev+1 到 i）

有 next - i 種終點，讓這個字元是最後一個（從 i 到 next-1）

所以這個出現的字元會出現在這些子字串中，且是唯一的（前面和後面沒有相同字元）

*/
