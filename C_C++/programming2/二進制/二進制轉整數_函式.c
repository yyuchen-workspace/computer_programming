#include <stdio.h>
#include <stdlib.h>

int main() {
    const char *binary_string = "1101"; // �o�O�G�i��r��
    int num;

    // �ϥ� strtol �N�G�i��r���ഫ�����
    num = (int)strtol(binary_string, NULL, 2); // '2' ��ܧڭ̴��Ѫ��O�G�i��榡

    printf("�G�i��G%s\n", binary_string);
    printf("��������ơG%d\n", num);

    return 0;
}
