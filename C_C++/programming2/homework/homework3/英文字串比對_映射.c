#include <stdio.h>
#include <string.h>

int main() {
    char order[27], S[101];
    scanf("%s", order);
    scanf("%s", S);

    int count[26] = {0};

    for (int i = 0; S[i]; i++) {
        count[S[i] - 'a']++;
    }

    for (int i = 0; order[i]; i++) {
        char c = order[i];
        while (count[c - 'a']-- > 0)
            putchar(c);
    }

    printf("\n");
    return 0;
}
