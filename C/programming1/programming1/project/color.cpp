#include <stdio.h>
#include <stdlib.h>

// 線性插值函數
int lerp(int start, int end, float t) {
    return (int)(start + t * (end - start));
}

// 設置RGB顏色的函數
void setRGB(int r, int g, int b) {
    printf("\033[38;2;%d;%d;%dm", r, g, b);
}

// 驗證RGB值是否合法
int validateRGB(int r, int g, int b) {
    return (r >= 0 && r <= 255 && g >= 0 && g <= 255 && b >= 0 && b <= 255);
}

int main() {
    int width, height;
    int tl_r, tl_g, tl_b; // 左上角RGB
    int tr_r, tr_g, tr_b; // 右上角RGB
    int bl_r, bl_g, bl_b; // 左下角RGB
    int br_r, br_g, br_b; // 右下角RGB

    // 輸入寬度與高度
    do {
        printf("Please enter the width (10-80): ");
        scanf("%d", &width);
    } while (width < 10 || width > 80);

    do {
        printf("Please enter the height (10-20): ");
        scanf("%d", &height);
    } while (height < 10 || height > 20);

    // 輸入四個角的RGB，並檢查是否有效
    do {
        printf("Please enter the top left RGB: ");
        scanf("%d,%d,%d", &tl_r, &tl_g, &tl_b);
    } while (!validateRGB(tl_r, tl_g, tl_b));

    do {
        printf("Please enter the top right RGB: ");
        scanf("%d,%d,%d", &tr_r, &tr_g, &tr_b);
    } while (!validateRGB(tr_r, tr_g, tr_b));

    do {
        printf("Please enter the bottom left RGB: ");
        scanf("%d,%d,%d", &bl_r, &bl_g, &bl_b);
    } while (!validateRGB(bl_r, bl_g, bl_b));

    do {
        printf("Please enter the bottom right RGB: ");
        scanf("%d,%d,%d", &br_r, &br_g, &br_b);
    } while (!validateRGB(br_r, br_g, br_b));

    // 顯示漸層效果
    for (int y = 0; y < height; y++) {
        float ty = (float)y / (height - 1); // 高度的比例

        // 插值計算兩個邊的顏色
        int left_r = lerp(tl_r, bl_r, ty);
        int left_g = lerp(tl_g, bl_g, ty);
        int left_b = lerp(tl_b, bl_b, ty);
        int right_r = lerp(tr_r, br_r, ty);
        int right_g = lerp(tr_g, br_g, ty);
        int right_b = lerp(tr_b, br_b, ty);

        for (int x = 0; x < width; x++) {
            float tx = (float)x / (width - 1); // 寬度的比例

            // 插值計算每一點的顏色
            int r = lerp(left_r, right_r, tx);
            int g = lerp(left_g, right_g, tx);
            int b = lerp(left_b, right_b, tx);

            // 設置該點的顏色
            setRGB(r, g, b);
            printf("█"); // 使用「█」字符來繪製顏色方塊
        }
        printf("\033[0m\n"); // 重置顏色並換行
    }

    return 0;
}
