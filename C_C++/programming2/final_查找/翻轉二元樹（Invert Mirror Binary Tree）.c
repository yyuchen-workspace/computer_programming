
TreeNode* invertTree(TreeNode* root) {
    if (!root) return NULL;
    TreeNode* temp = root->left;
    root->left = invertTree(root->right);
    root->right = invertTree(temp);
    return root;
}
