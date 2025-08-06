#include <stdio.h>
#include <stdint.h>

// �禡�Ω�N 16 ��L�Ÿ�����ഫ���G�i��榡�æL�X
void printBinary(uint16_t hexValue) {
    for (int i = 15; i >= 0; i--) {
        printf("%d", (hexValue >> i) & 1);  // �����C�Ӧ줸�ÿ�X
        if (i % 4 == 0) {  // �C 4 ��W�[�@�ӪŮ�A��K�\Ū
            printf(" ");
        }
    }
    printf("\n");
}

// �ഫ�����Ÿ���ơ]Signed Integer�^
int16_t toSignedInt(uint16_t hexValue) {
    // �P�_�Ÿ���O�_�� 1�A�p�G�� 1�A��ܭt�ơA�ϥΨ�ɼƪ�ܪk
    if ((hexValue & 0x8000) != 0) {  // �ˬd�̰���]�Ÿ���^
        return (int16_t)(hexValue - 0x10000);  // ��ɼ��ഫ
    }
    return (int16_t)hexValue;  // ���ƪ����ഫ
}

// �ഫ���B�I�ơ]Float�^
void toFloat(uint16_t hexValue) {
    int sign = (hexValue >> 15) & 1;  // �Ÿ���]S�^
    int exponent = (hexValue >> 10) & 0x1F;  // ���Ʀ�]5 ��^
    int fraction = hexValue & 0x3FF;  // �p�Ʀ�]10 ��^

    // �ഫ���B�I�ƪ���ǰO����ܪk S(1.F) * 2^(EXP - 15)
    double mantissa = 1.0;
    for (int i = 0; i < 10; i++) {
        if ((fraction >> (9 - i)) & 1) {
            mantissa += 1.0 / (1 << (i + 1));
        }
    }

    int actualExponent = exponent - 15;
    if (sign == 1) {
        mantissa = -mantissa;
    }

    // ��X����ǰO����ܪk
    printf("Converted float is: %.6f*2^%d\n", mantissa, actualExponent);
}

int main() {
    uint16_t hexValue;
    int outputType;

    // Ū���Q���i��Ʀr
    printf("Please input a hex: ");
    scanf("%x", &hexValue);

    // Ū���ϥΪ̿�ܪ���X����
    printf("Please choose the output type(1:integer ,2:unsigned integer ,3:float):");
    scanf("%d", &outputType);

    // ��X�G�i��榡
    printf("Binary of %X is: ", hexValue);
    printBinary(hexValue);

    // �ھڿ�ܪ������i��������ഫ
    switch (outputType) {
        case 1:  // ���Ÿ���ơ]Signed Integer�^
            printf("Converted signed integer is: %d\n", toSignedInt(hexValue));
            break;
        case 2:  // �L�Ÿ���ơ]Unsigned Integer�^
            printf("Converted unsigned integer is: %u\n", hexValue);
            break;
        case 3:  // �B�I�ơ]Float�^
            toFloat(hexValue);
            break;
        default:
            printf("Invalid output type.\n");
            break;
    }

    return 0;
}
