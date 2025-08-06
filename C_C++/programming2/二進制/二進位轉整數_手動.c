#include <stdio.h>
#include <string.h>

int binary_to_int(const char *binary_string) {
    int num = 0;
    int length = strlen(binary_string);

    // �M���r��A�p��C�@�쪺��
    for (int i = 0; i < length; i++) {
        num = num * 2 + (binary_string[i] - '0');
    }

    return num;
}

int main() {
    const char *binary_string = "1101"; // �G�i��r��
    int num;

    num = binary_to_int(binary_string); // ����ഫ�����

    printf("�G�i��G%s\n", binary_string);
    printf("��������ơG%d\n", num);

    return 0;
}

