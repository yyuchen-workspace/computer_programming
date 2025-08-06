#include <stdio.h>

void print_binary(unsigned char num) {
    printf("�G�i��G");
    for (int i = 7; i >= 0; i--) {
        printf("%d", (num >> i) & 1);
    }
    printf("\n");
}

int main() {
    unsigned char value;

    printf("�п�J�@�� 0~255 ����ơG");
    scanf("%hhu", &value);

    printf("�Q�i��G%u\n", value);
    print_binary(value);

    return 0;
}
