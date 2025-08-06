#include <stdio.h>

int main()
{
    char name[5][10] = {0};  // 存储 5 个学生姓名，每个姓名最多 9 个字符（预留 1 个位置给 '\0'）
    int score[5][4] = {0};   // 存储 5 个学生的分数数据，每个学生有 3 个分数和 1 个平均分

    for (int i = 0; i < 5; i++)
    {
        printf("Please enter student's name: ");
        scanf("%9s", name[i]); // 限制字符串长度，并检查返回值
        printf("Please enter three scores: ");

        // 打印 i 的值，确认它在合法范围内
        printf("Debug: i = %d\n", i);

        // 检查输入是否正确匹配 3 个整数
        scanf("%d %d %d", &score[i][0], &score[i][1], &score[i][2]);

        // 计算平均分
        score[i][3] = (score[i][0] + score[i][1] + score[i][2]) / 3;
        printf("Average for %s is %d\n", name[i], score[i][3]);
    }

    return 0;
}

