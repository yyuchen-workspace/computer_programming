#include<stdio.h>

int main()
{
    float f;
    scanf("%f", &f);
    int i;
    i = *((int *) &f);
    i = (i >> 23) & 0xFF;  // �k��23���A���X�� 8 ��
    printf("%d", i);
}
