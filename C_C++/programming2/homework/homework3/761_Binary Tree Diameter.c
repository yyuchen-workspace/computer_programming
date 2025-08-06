#include <stdio.h>
#include <stdlib.h>

#define MAXN 50

typedef struct Node {
    int left;
    int right;
} Node;

Node tree[MAXN];
int diameter = 0;

// 遞迴函式：傳回某節點的高度，並更新全域變數 diameter
int getHeight(int current) {
    if (current == -1)
        return 0;

    int leftH = getHeight(tree[current].left);
    int rightH = getHeight(tree[current].right);

    if (leftH + rightH > diameter)
        diameter = leftH + rightH;

    return (leftH > rightH ? leftH : rightH) + 1;
}

int main() {
    int N;
    scanf("%d", &N);

    for (int i = 0; i < N; i++) {
        int a, b;
        scanf("%d %d", &a, &b);
        tree[i].left = a;
        tree[i].right = b;
    }

    getHeight(0);  // 從根節點開始遞迴
    printf("%d\n", diameter);

    return 0;
}

