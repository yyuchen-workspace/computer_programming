#include<stdio.h>

int main()
{
    int times, height, frequency;
    scanf("%d", &times);

    for(int i = 0 ; i < times ; i++)//�X���ƥ�
    {
        scanf("%d%d", &height, &frequency);

        for(int j = 0 ; j < frequency ; j++)//�X�ӤT����
        {
            for(int k = 1 ; k <= height ; k++)//�X��
            {
                for(int l = k ; l > 0 ; l--)//����
                {
                    printf("%d", k);
                }
                printf("\n");
            }

            for(int k = height - 1 ; k > 0 ; k--)//�X��
            {
                for(int l = k ; l > 0 ; l--)//����
                {
                    printf("%d", k);
                }
                printf("\n");
            }
            if(j < frequency - 1)
            {
                printf("\n");
            }

        }

    }
    return 0;

}
