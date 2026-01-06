#include<stdio.h>
int main(){
    int A = 0, B = 0, C = 0;
    int n = 10;
    for (int i=0; i<n; i++) {
        A++;
        for (int j=i; j<n; j++){
            B++;
            for (int k=j; k<n; k++){
                C++;

            }
        }
           
    }
       
        printf("A = %d, B = %d, C = %d", A, B, C);
                 
}


