#include <stdio.h>
#include <math.h>

typedef struct {
    double x, y;
} Vector;

// 向量加法
Vector vector_add(Vector v1, Vector v2) {
    v1.x+=v2.x, v1.y+=v2.y;
    return v1;
}

// 向量減法
Vector vector_sub(Vector v1, Vector v2) {
    v1.x-=v2.x, v1.y-=v2.y;
    return v1;
}

// 向量內積
double vector_dot(Vector v1, Vector v2) {
    return v1.x*v2.x + v1.y*v2.y;
}

// 向量長度 你可以使用畢氏定理計算
double vector_magnitude(Vector v) {
    return sqrt(v.x*v.x+v.y*v.y);
}

// 單位向量 = (x / 向量長度, y / 向量長度)
// 注意：如果向量長度為 0，則返回原向量
Vector vector_normalize(Vector v) {
    double m = vector_magnitude(v);

    if(m==0)return v;
    v.x/=m, v.y/=m;
    return v;
}

int main() {
    Vector A, B, res;
    char op;
    scanf("%lf %lf\n", &A.x, &A.y);
    scanf("%lf %lf\n", &B.x, &B.y);
    scanf("%c", &op);

    switch(op){
        case 'a':
            res = vector_add(A, B);
            printf("(%lf, %lf)", res.x, res.y);
            break;
        case 's':
            res = vector_sub(A, B);
            printf("(%lf, %lf)", res.x, res.y);
            break;
        case 'd':
            printf("%lf", vector_dot(A, B));
            break;
        case 'm':
            printf("%lf", vector_magnitude(A));
            break;
        case 'n':
            res = vector_normalize(A);
            printf("(%lf, %lf)", res.x, res.y);
            break;
    }

    return 0;
}
