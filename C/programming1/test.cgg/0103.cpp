#include <stdio.h>
#include <stdlib.h>

int main() {
    int x1, y1, x2, y2;
    double m, c, xx, yy, area;

    // 輸入點 A 的座標
    printf("Please enter the point A (x,y): ");
    if (scanf("%d,%d", &x1, &y1) != 2) {
        printf("Error: Invalid input for point A.\n");
        return 1;
    }

    // 輸入點 B 的座標
    printf("Please enter the point B (x,y): ");
    if (scanf("%d,%d", &x2, &y2) != 2) {
        printf("Error: Invalid input for point B.\n");
        return 1;
    }

    // 檢查是否形成有效直線
    if (x1 == x2 && y1 == y2) {
        printf("Error: Points A and B must not be the same.\n");
        return 1;
    }

    // 計算斜率 m 和截距 c
    m = (double)(y2 - y1) / (x2 - x1);
    c = y1 - m * x1;

    // 計算與 x 軸和 y 軸的交點
    xx = -c / m;
    yy = c;

    // 計算三角形面積
    area = 0.5 * (xx * yy);

    // 輸出面積結果，保留兩位小數
    if (area == 0) {
        printf("Error: Area is 0.\n");
        return 1;
    }

    printf("Area: %.2f\n", area);

    return 0;
}












