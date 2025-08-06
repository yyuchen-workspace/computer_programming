//條件：左右子樹高度差不超過 1，且子樹也平衡


int checkBalance(TreeNode* root) {
    if (!root) return 0;
    int lh = checkBalance(root->left);
    if (lh == -1) return -1;
    int rh = checkBalance(root->right);
    if (rh == -1) return -1;
    if (abs(lh - rh) > 1) return -1;
    return 1 + (lh > rh ? lh : rh);
}

bool isBalanced(TreeNode* root) {
    return checkBalance(root) != -1;
}
