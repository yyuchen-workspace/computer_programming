#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode{
	int val;
	struct TreeNode* left;
	struct TreeNode* right;
}TreeNode;

TreeNode* getTree(int seed) {
    const int SIZE = seed^0x168;
    TreeNode* nodes[SIZE];

    for (int i = 0; i < SIZE; i++) {
        unsigned int x = (unsigned int)seed;
        unsigned int t = x * 2654435761u;
        t ^= (i * 0x9e3779b1u);
        t  = (t >> 13) ^ (t << 7);
        int v = (int)(t % 101) - 50;

        nodes[i] = malloc(sizeof(TreeNode));
        nodes[i]->val   = v;
        nodes[i]->left  = NULL;
        nodes[i]->right = NULL;
    }

    for (int i = 0; i < SIZE; i++) {
        int li = 2*i + 1, ri = 2*i + 2;
        if (li < SIZE) nodes[i]->left  = nodes[li];
        if (ri < SIZE) nodes[i]->right = nodes[ri];
    }

    return nodes[0];
}

void averageTree(TreeNode* root, int level, int levelCount[], int levelSum[]) {
    if (root == NULL) {
        return;
    }

    levelSum[level] += root->val;
    levelCount[level]++;

    averageTree(root->left, level + 1, levelCount, levelSum);
    averageTree(root->right, level + 1, levelCount, levelSum);
}

int main() {
	int n, res;
	scanf("%d", &n);

	TreeNode* root = getTree(n);

	int levelSum[10000] = {0};
	int levelCount[10000] = {0};
	averageTree(root, 0, levelCount, levelSum);

	int i = 0;
	while (levelCount[i] != 0) {
		printf("%.2lf ", ((double)levelSum[i] / (double)levelCount[i]));
		i++;
	}
	return 0;
}
