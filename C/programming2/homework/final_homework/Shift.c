//�`�NACII�۴�i�H�O�t���A�ӭ^��r����26�`��

#include<stdio.h>
#include<string.h>

int main()
{
    char before[21];
    char after[21];

    scanf("%s", before);
    scanf("%s", after);

    if(strlen(before) !=  strlen(after))
    {
            printf("False\n");
            return 0;
    }
    int distance = (before[0] - after[0] + 26) % 26;

    for(int i = 0 ; i < strlen(before) ; i++)
    {

        if(distance != (before[i] - after[i] + 26) % 26)
        {
            printf("False\n");
            return 0;
        }
    }

     printf("True\n");
     return 0;
}
