#include <stdio.h>
#include <math.h>

typedef struct {
    double x, y;
} Vector;

// �V�q�[�k
Vector vector_add(Vector v1, Vector v2) {
    v1.x+=v2.x, v1.y+=v2.y;
    return v1;
}

// �V�q��k
Vector vector_sub(Vector v1, Vector v2) {
    v1.x-=v2.x, v1.y-=v2.y;
    return v1;
}

// �V�q���n
double vector_dot(Vector v1, Vector v2) {
    return v1.x*v2.x + v1.y*v2.y;
}

// �V�q���� �A�i�H�ϥβ���w�z�p��
double vector_magnitude(Vector v) {
    return sqrt(v.x*v.x+v.y*v.y);
}

// ���V�q = (x / �V�q����, y / �V�q����)
// �`�N�G�p�G�V�q���׬� 0�A�h��^��V�q
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
