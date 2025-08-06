//使用堆疊進行 DFS（不使用遞迴）
//適用於圖、迷宮等遍歷問題
/*
0 - 1 - 2
    |
    3
*/

#include <stdio.h>

#define V 4
int graph[V][V] = {
    {0,1,0,0},
    {1,0,1,1},
    {0,1,0,0},
    {0,1,0,0}
};

int stack[V], top = -1, visited[V] = {0};

void dfs(int start) {
    stack[++top] = start;

    while (top != -1) {
        int v = stack[top--];
        if (!visited[v]) {
            printf("%d ", v);
            visited[v] = 1;
            for (int i = V-1; i >= 0; i--) {
                if (graph[v][i] && !visited[i]) {
                    stack[++top] = i;
                }
            }
        }
    }
}

int main() {
    printf("DFS traversal from node 0: ");
    dfs(0);
    printf("\n");
    return 0;
}
