#include <stdio.h>
#include <stdlib.h>

typedef struct _node {
    struct _node* left;
    struct _node* right;
} Node;

int maxDiameter = 0;

int getHeightAndUpdateDiameter(Node* root) {
    if (root == NULL) return 0;
    int left = getHeightAndUpdateDiameter(root->left);
    int right = getHeightAndUpdateDiameter(root->right);
    if (left + right > maxDiameter)
        maxDiameter = left + right;
    return (left > right ? left : right) + 1;
}

int main() {
    int n;
    scanf("%d", &n);

    Node nodes[51];
    for (int i = 0; i < n; i++) {
        nodes[i].left = NULL;
        nodes[i].right = NULL;
    }

    for (int i = 0; i < n; i++) {
        int l, r;
        scanf("%d %d", &l, &r);
        if (l != -1)
            nodes[i].left = &nodes[l];
        if (r != -1)
            nodes[i].right = &nodes[r];
    }

    getHeightAndUpdateDiameter(&nodes[0]);
    printf("%d\n", maxDiameter);
    return 0;
}

/*
�o�q���j�����ơG

��X�H�C�Ӹ`�I���ڪ��l�𪺰���

�P�ɭp��q������e���k���̪����|�]�]�N�O�i�઺���|�^
*/
