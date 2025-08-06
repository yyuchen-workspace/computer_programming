#include "mymath.h"
#include "mygraph.h"
#include <stdio.h>
#include<stdlib.h>
#include<stdint.h>
#include<time.h>

int main()
{
    srand(time(0));
    int32_t v = UniformRand(0, 100); // return a random value in [0, 100]
    if (IsOdd(v))
    {
        printf("%d is odd.\n", v);
    }

    if (IsPrime(v))
    {
        printf("%d is prime.\n", v);
    }

    printf("Square %d is %d\n", v, Square(v));

    printf("The Euclidean distance between (0, 0) and (1, 2) is %f\n", EuclideanDistance(0, 0, 1, 2));

    int32_t len, row, col;
    printf("Input the length you want: ");
    scanf("%d", &len);
    DrawLine(len);
    printf("\n");

    printf("Input the row and column you want: ");
    scanf("%d%d", &row, &col);
    DrawRectangle(row, col);

    printf("Input the length you want: ");
    scanf("%d", &len);
    DrawSquare(len);
}
