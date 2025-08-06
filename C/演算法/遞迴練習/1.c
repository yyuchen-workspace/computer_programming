#include <stdio.h>

/*
 * 遞迴思考的核心框架：
 * 1. 找出基礎情況 (Base Case)
 * 2. 找出遞迴關係 
 * 3. 確保收斂性
 * 4. 組合解答
 */

// 範例1: 階乘
int factorial(int n) {
    // 基礎情況
    if (n <= 1) {
        printf("Base case: %d! = 1\n", n);
        return 1;
    }
    
    // 遞迴情況
    printf("Computing %d! = %d * (%d-1)!\n", n, n, n);
    int result = n * factorial(n - 1);
    printf("Result: %d! = %d\n", n, result);
    return result;
}

// 範例2: 費波那契
int fibonacci(int n) {
    printf("Enter F(%d)\n", n);
    
    if (n == 0) return 0;
    if (n == 1) return 1;
    
    printf("F(%d) = F(%d) + F(%d)\n", n, n-1, n-2);
    int result = fibonacci(n - 1) + fibonacci(n - 2);
    printf("F(%d) = %d\n", n, result);
    return result;
}

// 範例3: 陣列求和
int array_sum(int arr[], int n) {
    if (n == 0) return 0;
    
    printf("sum[%d] = %d + sum[%d]\n", n, arr[0], n-1);
    return arr[0] + array_sum(arr + 1, n - 1);
}

int main() {
    printf("=== Recursion Thinking Demo ===\n\n");
    
    printf("1. Factorial 4!:\n");
    int fact = factorial(4);
    printf("Result: %d\n\n", fact);
    
    printf("2. Fibonacci F(4):\n");
    int fib = fibonacci(4);
    printf("Result: %d\n\n", fib);
    
    printf("3. Array sum:\n");
    int arr[] = {1, 2, 3, 4, 5};
    int sum = array_sum(arr, 5);
    printf("Result: %d\n", sum);
    
    return 0;
}