#include<stdio.h>
void hanoi(int n, char src, char dst, char buffer) {
    if (n == 1)
        printf("%d from %c to %c\n", n, src, dst);
    else {
        hanoi(n - 1, src, buffer, dst);
        printf("%d from %c to %c\n", n, src, dst);
        hanoi(n - 1, buffer, dst, src);
    }
}

int main(void) {
  int n;
  scanf("%d", &n);
  hanoi(n, 'A', 'C', 'B');
  return 0;
}
