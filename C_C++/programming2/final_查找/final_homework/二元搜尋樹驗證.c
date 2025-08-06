#include<stdio.h>
#include<stdbool.h>
#include <limits.h>

typedef struct{
    int left;
    int right;
    int data;
} Node;
Node tree[100005];

bool is_BST(int id, int min, int max)
{
    if(id == -1)return true;
    int val = tree[id].data;
    if(val <= min || val >= max)
    {
        return false;
    }

    return is_BST(tree[id].left, min, val) && is_BST(tree[id].right, val, max);
}


int main()
{
    int N;
    scanf("%d", &N);

    for(int i = 0 ; i < N ; i++)
    {
        scanf("%d%d%d", &tree[i].left, &tree[i].right, &tree[i].data);
    }

    bool is_bst = is_BST(0, INT_MIN, INT_MAX);
    if(is_bst)
    {
        printf("YES\n");
    }
    else
    {
        printf("NO\n");
    }
}
