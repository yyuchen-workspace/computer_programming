#include <stdio.h>
int main()
{
int T = 0;
scanf("%d", &T);
for (int t=0; t<T; t+=1)
{
char plate[10]={};
scanf("%s", plate);
int first = 0, second = 0;
for (int i=0; i<3; i+=1) // 盢玡璣ゅダ锣Θ计
{
first = first*26 + (plate[i]-'A');
}
for (int i=4; i<8; i+=1) // 盢程计じㄖΘ计
{
second = second*10 + (plate[i]-'0');
}
int diff = (first>=second ? first-second : second-first);
if (diff <= 100)
{
puts("nice");
}
else
{
puts("not nice");
}
}
}
