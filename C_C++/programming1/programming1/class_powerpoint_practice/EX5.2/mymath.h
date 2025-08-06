#ifndef MY_MATH
#define MY_MATH

#include<stdio.h>
#include<stdint.h>
#include<stdbool.h>
#include<math.h>

bool IsOdd(int32_t v);
bool IsPrime(int32_t v);
int32_t Square(int32_t v);
int UniformRand(int32_t lb, int32_t ub); // [lb, ub]
double EuclideanDistance(int32_t x1, int32_t y1, int32_t x2, int32_t y2);


#endif
