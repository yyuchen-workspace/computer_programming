#include<stdio.h>
#include<stdint.h>
#include<stdbool.h>
#include<math.h>

bool IsOdd(int32_t v)
{
    return  (v % 2 == 1);

}


bool IsPrime(int32_t v)
{
    if(v <= 1) return false;
    if(v == 2) return true;
    if (v % 2 == 0) return false;
    for(int i = 3; i < sqrt(v) ; i+=2 )
    {
        if( v % i == 0)
        {
            return false;
        }
    }

    return true;
}


int32_t Square(int32_t v)
{
    v *= v;
    return v;
}


int32_t UniformRand(int32_t lb, int32_t ub)
{
    return lb + rand() % (ub - lb + 1);
}


double EuclideanDistance(int x1, int y1, int x2, int y2)
{
    return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
}

