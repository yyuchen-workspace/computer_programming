#include<stdio.h>
#include <string.h>
#define max 101


typedef struct {
    char ch;
    int count;
} StackElement;

/*每個元素記錄：字元 + 出現次數

可應付像「三消遊戲」、「連鎖合併」這種要追蹤「連續出現幾個」的邏輯

彈性高，可擴充更多欄位（例如時間戳、位置等）*/


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
