#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode {
    int val;
    struct TreeNode* left;
    struct TreeNode* right;
} TreeNode;

// �w�q queue �`�I�]��@�����^
typedef struct QueueNode {
    TreeNode* treeNode;
    struct QueueNode* next;
} QueueNode;

// �w�q queue ����
typedef struct {
    QueueNode* front;
    QueueNode* rear;
} Queue;

// ��l�� queue
Queue* createQueue() {
    Queue* q = (Queue*)malloc(sizeof(Queue));
    q->front = q->rear = NULL;
    return q;
}

// �[�J queue
void enqueue(Queue* q, TreeNode* node) {
    QueueNode* temp = (QueueNode*)malloc(sizeof(QueueNode));
    temp->treeNode = node;
    temp->next = NULL;

    if (q->rear == NULL) {
        q->front = q->rear = temp;
        return;
    }

    q->rear->next = temp;
    q->rear = temp;
}

// ���X queue
TreeNode* dequeue(Queue* q) {
    if (q->front == NULL) return NULL;

    QueueNode* temp = q->front;
    TreeNode* treeNode = temp->treeNode;

    q->front = q->front->next;
    if (q->front == NULL) q->rear = NULL;

    free(temp);
    return treeNode;
}

// �ˬd queue �O�_����
int isEmpty(Queue* q) {
    return q->front == NULL;
}

// ������ queue
void freeQueue(Queue* q) {
    while (!isEmpty(q)) dequeue(q);
    free(q);
}


void printLevelOrder(TreeNode* root) {
    if (!root) return;

    Queue* q = createQueue();
    enqueue(q, root);

    while (!isEmpty(q)) {
        TreeNode* node = dequeue(q);
        printf("%d ", node->val);

        if (node->left) enqueue(q, node->left);
        if (node->right) enqueue(q, node->right);
    }

    printf("\n");
    freeQueue(q);
}

TreeNode* insert(TreeNode* root, int val) {
    if (!root) {
        TreeNode* node = malloc(sizeof(TreeNode));
        node->val = val;
        node->left = node->right = NULL;
        return node;
    }
    if (val < root->val) root->left = insert(root->left, val);
    else if (val > root->val) root->right = insert(root->right, val);
    return root;
}

int main() {
    TreeNode* root = NULL;
    int vals[] = {50, 30, 70, 20, 40, 60, 80};

    for (int i = 0; i < 7; i++)
        root = insert(root, vals[i]);

    printf("Level-order traversal (BFS):\n");
    printLevelOrder(root);

    return 0;
}
