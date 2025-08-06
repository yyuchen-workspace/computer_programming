#include <stdio.h>
#include "mychar.h"

int main() {
    char test_char = 'a';
    //char test_char = 'A';
    //char test_char = '1';
    printf("islower2('%c') = %d\n", test_char, islower2(test_char));
    printf("isupper2('%c') = %d\n", test_char, isupper2(test_char));
    printf("isalpha2('%c') = %d\n", test_char, isalpha2(test_char));
    printf("isdigit2('%c') = %d\n", test_char, isdigit2(test_char));
    printf("toupper2('%c') = '%c'\n", test_char, toupper2(test_char));
    printf("tolower2('%c') = '%c'\n", test_char, tolower2(test_char));

    return 0;
}
