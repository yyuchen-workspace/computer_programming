#include <stdio.h>
#include <string.h>
#define SIZE 20

void printIncreasingNDigits(int n, int cur, int last, char* output){
	if(cur==n){
		printf("%s ", output);
		return;
	}

	for(int i=last+1; i<=9; i++){
		output[cur] = i+48;
		printIncreasingNDigits(n, cur+1, i, output);
	}
}

int main(){
	int N;
	char str[SIZE]={0};
	scanf("%d", &N);

	printIncreasingNDigits(N, 0, -1, str);
}
