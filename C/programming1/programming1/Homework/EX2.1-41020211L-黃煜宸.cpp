#include<stdio.h>
int main()
{
	int a;
	int b;
	int sum[5];
	printf("Please input two integers ...> ");
	scanf("%d %d", &a, &b);
    sum[0] = a + b;
    sum[1] = a - b;
    sum[2] = a * b;
	if(b == 0)
	{
		printf("Please input the second operand again...>");
		scanf("%d", &b);

			if(b == 0)
            {
                printf("Hey do you know what I said?");
                return 0;
            }

    }

    sum[3] = a / b;
    sum[4] = a % b;
    printf("%d + %d = %d\n", a, b, sum[0]);
    printf("%d - %d = %d\n", a, b, sum[1]);
    printf("%d * %d = %d\n", a, b, sum[2]);
    printf("%d / %d = %d\n", a, b, sum[3]);
    printf("%d %% %d = %d\n", a, b, sum[4]);




    return 0;

}
