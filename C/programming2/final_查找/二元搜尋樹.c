typedef struct TreeNode {
    int val;
    struct TreeNode* left;
    struct TreeNode* right;
} TreeNode;

TreeNode* insert(TreeNode* root, int val) {
    if (root == NULL) {
        TreeNode* node = malloc(sizeof(TreeNode));
        node->val = val;
        node->left = node->right = NULL;
        return node;
    }
    if (val < root->val) root->left = insert(root->left, val);
    else if (val > root->val) root->right = insert(root->right, val);
    return root;
}

TreeNode* search(TreeNode* root, int val) {
    if (!root || root->val == val) return root;
    if (val < root->val) return search(root->left, val);
    return search(root->right, val);
}

int main() {
    TreeNode* root = NULL;

    // 插入節點
    root = insert(root, 50);
    insert(root, 30);
    insert(root, 70);
    insert(root, 20);
    insert(root, 40);
    insert(root, 60);
    insert(root, 80);

    // 查詢是否有值 40
    TreeNode* found = search(root, 40);
    if (found) printf("Found: %d\n", found->val);
    else printf("Not found.\n");

    return 0;
}
