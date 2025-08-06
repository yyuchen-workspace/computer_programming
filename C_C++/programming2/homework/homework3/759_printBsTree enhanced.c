/* tree */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>  // ���F�ϥ� strcpy ��

struct treenode {
  int data;
  struct treenode *left;
  struct treenode *right;
};
typedef struct treenode TreeNode;

/* genNode */
TreeNode *genTreeNode(int data, TreeNode *left, TreeNode *right)
{
  TreeNode *node = malloc(sizeof(TreeNode));
  assert(node != NULL);
  node->data = data;
  node->left = left;
  node->right = right;
  return node;
}

/* print - ��}���� */
void printBsTreeHelper(TreeNode *root, const char *path, int depth)
{
  if (root == NULL)
    return;

  // ���l��G�[�J 'L'
  char leftPath[100];
  snprintf(leftPath, sizeof(leftPath), "%sL", path);
  printBsTreeHelper(root->left, leftPath, depth + 1);

  // ��X�ثe�`�I��T
  if (depth == 0)
    printf("0 data = %d\n", root->data);  // �ڸ`�I
  else
    printf("%s%d data = %d\n", path, depth, root->data);

  // �k�l��G�[�J 'R'
  char rightPath[100];
  snprintf(rightPath, sizeof(rightPath), "%sR", path);
  printBsTreeHelper(root->right, rightPath, depth + 1);
}

void printBsTree(TreeNode *root)
{
  printBsTreeHelper(root, "", 0);
}

/* insert */
TreeNode *insertBsTree(TreeNode *root, int data)
{
  if (root == NULL)
    return genTreeNode(data, NULL, NULL);

  if (data < root->data)
    root->left = insertBsTree(root->left, data);
  else
    root->right = insertBsTree(root->right, data);
  return root;
}

/* free */
void freeTree(TreeNode *root)
{
  if (root == NULL)
    return;
  else {
    freeTree(root->left);
    freeTree(root->right);
    free(root);
  }
}

/* main */
#define KEYS 5
int main(void)
{
  int insertKeys[KEYS];
  for (int i = 0; i < KEYS; i++)
    scanf("%d", &(insertKeys[i]));

  TreeNode *root = NULL;
  for (int i = 0; i < KEYS; i++)
    root = insertBsTree(root, insertKeys[i]);

  printBsTree(root);

  freeTree(root);
  return 0;
}
