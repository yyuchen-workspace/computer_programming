
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

int main()
{
    char encrypted[100] = {};
    while ((scanf("%s", encrypted) != EOF))
    {
        int cnt_e[26] = {}; // �O���[�K�������C�Ӧr�����W�v
        int length_e = strlen(encrypted);
        int repeat_e[length_e + 1]; // �O���C���W�v�X�{������
        memset(repeat_e, 0, sizeof(repeat_e));

        for (int i = 0; i < length_e; i++)
        {
            cnt_e[encrypted[i] - 'A'] += 1; // �ϥ� 'A' �Ӥ��O 'a'
        }
        for (int i = 0; i < 26; i++)
        {
            if (cnt_e[i] > 0) // �T�O�W�v����
            {
                repeat_e[cnt_e[i]] += 1;
            }
        }

        char original[100] = {};
        scanf("%s", original);
        int length_o = strlen(original);
        int cnt_o[26] = {}; // �O����l�������C�Ӧr�����W�v
        int repeat_o[length_o + 1]; // �O���C���W�v�X�{������
        memset(repeat_o, 0, sizeof(repeat_o));

        for (int i = 0; i < length_o; i++)
        {
            cnt_o[original[i] - 'A'] += 1;
        }
        for (int i = 0; i < 26; i++)
        {
            if (cnt_o[i] > 0) // �T�O�W�v����
            {
                repeat_o[cnt_o[i]] += 1;
            }
        }

        // �������W�v���G�O�_�۵�
        bool repeated = true;
        for (int i = 0; i <= length_e && repeated; i++) // ����d������ 0 ~ length_e
        {
            if (repeat_e[i] != repeat_o[i])
            {
                repeated = false;
            }
        }

        if (repeated)
        {
            printf("YES\n");
        }
        else
        {
            printf("NO\n");
        }
    }
    return 0;
}
