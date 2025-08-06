#include <stdio.h>
#include <stdbool.h>

int main() {
    char guess[6], answer[6], result[6];
    scanf("%s %s", guess, answer);

    bool used_in_answer[5] = { false };  // �аO���������Ǧr���Q�ϥιL
    bool used_in_guess[5] = { false };   // �аO�q�������Ǧr���w�Q�B�z
    int i, j;

    // �Ĥ@���M���A�B�z���r��
    for (i = 0; i < 5; i++) {
        if (guess[i] == answer[i]) {
            result[i] = 'G';
            used_in_guess[i] = true;
            used_in_answer[i] = true;
        }
    }

    // �ĤG���M���A�B�z����r��
    for (i = 0; i < 5; i++) {
        if (result[i] != 'G') {  // �u�����O��⪺�~�ˬd
            for (j = 0; j < 5; j++) {
                if (guess[i] == answer[j] && !used_in_answer[j] && !used_in_guess[i]) {
                    result[i] = 'Y';
                    used_in_answer[j] = true;
                    used_in_guess[i] = true; // �O���w�g�B�z���r��
                    break;
                }
            }
        }
    }

    // �ĤT���M���A�B�z�զ�r��
    for (i = 0; i < 5; i++) {
        if (result[i] != 'G' && result[i] != 'Y') {
            result[i] = '-';
        }
    }

    // ��X���G
    for (i = 0; i < 5; i++) {
        printf("%c", result[i]);
    }
    printf("\n");

    return 0;
}
