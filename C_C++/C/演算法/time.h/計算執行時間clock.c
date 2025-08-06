#include <stdio.h>
#include <time.h>


void function1()
{
    printf("hello world\n");
}


int main()
{
    double Runtime;
    long start,end;
    start = clock();
    function1();
    end = clock();
    Runtime = difftime(end, start);
    //等價於Runtime = ((double)(end - start)) / CLK_TCK;
    printf("Runtime: %f seconds\n", Runtime);
    return 0;
}   