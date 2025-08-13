#include <stdio.h>

int *findSubstring(char *s, char **words, int wordsSize, int *returnSize)
{
    int s_length = strlen(s);
    int words_length = strlen(words[0]);
    int words_quantity = 0;
    int frequency = 0;

    while (words[words_quantity][0] != '\0')
    {
        words_quantity++;
    }
}
int main()
{
    char s[10000] = {"barfoothefoobarman"};
    char words[5000][30] = {"foo", "bar"};
    int wordsSize = 0;
    int returnSize = 0;
    findSubstring(s, words, wordsSize, returnSize);
}