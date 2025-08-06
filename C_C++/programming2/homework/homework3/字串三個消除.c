#include<stdio.h>
#include <string.h>
#define max 101


typedef struct {
    char ch;
    int count;
} StackElement;

/*�C�Ӥ����O���G�r�� + �X�{����

�i���I���u�T���C���v�B�u�s��X�֡v�o�حn�l�ܡu�s��X�{�X�ӡv���޿�

�u�ʰ��A�i�X�R��h���]�Ҧp�ɶ��W�B��m���^*/


int main()
{
    char input[max];
    StackElement stack[max];
    scanf("%s", input);

    int top = -1;
    int score = 0;

    for(int i = 0 ; input[i]!= '\0' ; i++)
    {
        char c = input[i];
        if(top == -1 || stack[top].ch != c)
        {
            stack[++top].ch = c;
            stack[top].count=1;
        }
        else
        {
            stack[top].count++;
            if(stack[top].count == 3)
            {
                top--;
                score++;
            }
        }
    }

    printf("%d\n", score);
    for (int i = 0; i <= top; i++) {
        for (int j = 0; j < stack[i].count; j++) {
            printf("%c", stack[i].ch);
        }
    }

}
