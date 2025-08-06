#include <stdio.h>
#include <stdlib.h>

#define MAXN 50

typedef struct Node {
    int left;
    int right;
} Node;

Node tree[MAXN];
int diameter = 0;

// ���j�禡�G�Ǧ^�Y�`�I�����סA�ç�s�����ܼ� diameter
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

    getHeight(0);  // �q�ڸ`�I�}�l���j
    printf("%d\n", diameter);

    return 0;
}

