#include <stdio.h>
#include <string.h>

int main() {
    char s[10001];
    scanf("%s", s);
    int len = strlen(s);
    long long total = 0;

    for (int i = 0; i < len; ++i) {
        int count[26] = {0};
        for (int j = i; j < len; ++j) {
            count[s[j] - 'a']++;

            // 計算目前這個子字串的獨特字元數量
            int unique = 0;
            for (int k = 0; k < 26; ++k) {
                if (count[k] == 1) unique++;
            }

            total += unique;
        }
    }

    printf("%lld\n", total);
    return 0;
}

