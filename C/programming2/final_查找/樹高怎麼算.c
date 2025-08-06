
int treeHeight(TreeNode* root) {
    if (!root) return 0;
    int l = treeHeight(root->left);
    int r = treeHeight(root->right);
    return 1 + (l > r ? l : r);
}
