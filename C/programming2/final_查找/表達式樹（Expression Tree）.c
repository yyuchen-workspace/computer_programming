//建構 + 計算
//節點為運算子或數字，後序（Postfix）建樹最方便。


typedef struct ExprNode {
    char op; // '+', '*', or '\0' for number
    int val;
    struct ExprNode *left, *right;
} ExprNode;

ExprNode* createValueNode(int val) {
    ExprNode* n = malloc(sizeof(ExprNode));
    n->op = '\0'; n->val = val;
    n->left = n->right = NULL;
    return n;
}

ExprNode* createOpNode(char op, ExprNode* l, ExprNode* r) {
    ExprNode* n = malloc(sizeof(ExprNode));
    n->op = op;
    n->left = l; n->right = r;
    return n;
}

int eval(ExprNode* root) {
    if (root->op == '\0') return root->val;
    int l = eval(root->left), r = eval(root->right);
    switch (root->op) {
        case '+': return l + r;
        case '-': return l - r;
        case '*': return l * r;
        case '/': return l / r;
    }
    return 0;
}
