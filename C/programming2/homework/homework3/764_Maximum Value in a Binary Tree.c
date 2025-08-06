
#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode{
	int val;
	struct TreeNode* left;
	struct TreeNode* right;
}TreeNode;

TreeNode* o_28a056b04461f9fad961d0e6a7494938(int o_ca3086beb9d047d8570ced588283aded, int o_1201404cd56c17518617d3c2afa5d81f, int o_25e9593a8cdc29d83875499532ad2773[])
{
	if ((o_1201404cd56c17518617d3c2afa5d81f > (0x000000000000000A + 0x0000000000000205 + 0x0000000000000805 - 0x0000000000000A0F)) & !!(o_1201404cd56c17518617d3c2afa5d81f > (0x000000000000000A + 0x0000000000000205 + 0x0000000000000805 - 0x0000000000000A0F)))return NULL;
	TreeNode* o_3730d340c3ab69a5ffec9f8f40d19c5d = malloc(sizeof(TreeNode));
	int o_50fdcd77f4e7e5851d29511359282b46 = o_25e9593a8cdc29d83875499532ad2773[(o_ca3086beb9d047d8570ced588283aded * o_ca3086beb9d047d8570ced588283aded) % (0x0000000000000014 + 0x000000000000020A + 0x000000000000080A - 0x0000000000000A1E)];
	o_3730d340c3ab69a5ffec9f8f40d19c5d->val = o_ca3086beb9d047d8570ced588283aded;
	o_3730d340c3ab69a5ffec9f8f40d19c5d->left = o_28a056b04461f9fad961d0e6a7494938(o_ca3086beb9d047d8570ced588283aded + o_50fdcd77f4e7e5851d29511359282b46, o_1201404cd56c17518617d3c2afa5d81f + (0x0000000000000002 + 0x0000000000000201 + 0x0000000000000801 - 0x0000000000000A03), o_25e9593a8cdc29d83875499532ad2773);
	o_3730d340c3ab69a5ffec9f8f40d19c5d->right = o_28a056b04461f9fad961d0e6a7494938(o_ca3086beb9d047d8570ced588283aded - o_50fdcd77f4e7e5851d29511359282b46, o_1201404cd56c17518617d3c2afa5d81f + (0x0000000000000002 + 0x0000000000000201 + 0x0000000000000801 - 0x0000000000000A03), o_25e9593a8cdc29d83875499532ad2773);
	return o_3730d340c3ab69a5ffec9f8f40d19c5d; };

TreeNode* getTree(int o_33e61257c56133bd9f2f1334b7db5eb0)
{
	int o_941fd8edfec1787ca107f660f8ce6faf[] = { -8,93,64,-38,16,-29,-33,-52,78, 2 };
	TreeNode* o_35fb3e4c1d75e97af5a9dafabcdd1874 = o_28a056b04461f9fad961d0e6a7494938(o_33e61257c56133bd9f2f1334b7db5eb0, (0x0000000000000002 + 0x0000000000000201 + 0x0000000000000801 - 0x0000000000000A03), o_941fd8edfec1787ca107f660f8ce6faf);
	return o_35fb3e4c1d75e97af5a9dafabcdd1874;
};

int findMax(TreeNode* root) {

    if (root == NULL) return -1;
    int max = root->val;
    int left = findMax(root->left);
    if(left > max)
        max = left;
    int right = findMax(root->right);
    if(right > max)
        max = right;
    return max;

}

int main() {
	int n, res;
	scanf("%d", &n);

	TreeNode* root = getTree(n);
	res = findMax(root);

	printf("%d", res);
	return 0;
}
