#include <stdio.h>
#include <string.h>
#include<ctype.h>
#define STRINGLEN 40

int s2n(char *s) {
   int n=0;

   while (*s != '\0') {
      n = n*10 + (*s - '0');
      s++;
   }
   return n;
};

int gcd(int a, int b) {
   if (a % b == 0) return b;
   return gcd(b, a%b);
};

typedef struct rational Rational;

struct rational {
  int num;
  int denom;
};

Rational add(Rational a, Rational b)
{
  Rational c;
  int g;
  c.num = a.num*b.denom + a.denom*b.num;
  c.denom = a.denom*b.denom;
  g = gcd(c.num, c.denom);
  c.num /= g;
  c.denom /= g;
  return c;
};

Rational sub(Rational a, Rational b)
{
  Rational c;
  int g;
  c.num = a.num*b.denom - a.denom*b.num;
  c.denom = a.denom*b.denom;
  g = gcd(c.num, c.denom);
  c.num /= g;
  c.denom /= g;
  return c;
};

Rational mul(Rational a, Rational b)
{
  Rational c;
  int g;
  c.num = a.num*b.num;
  c.denom = a.denom*b.denom;
  g = gcd(c.num, c.denom);
  c.num /= g;
  c.denom /= g;
  return c;
};


int main(void)
{
    char s[STRINGLEN];
    scanf("%s", s);
    char *op = strpbrk(s, "+-*");
    char temp_op = *op;
    Rational a, b, c;
    *op = '\0';
    char *slash_a = strchr(s, '/');  // 找到 '/' 位置
    *slash_a = '\0';  // 把 '/' 替換為 '\0'，將字串拆開
    a.num = s2n(s);  // 轉換分子
    a.denom = s2n(slash_a + 1);
    char *slash_b = strchr(op+1, '/');
    *slash_b = '\0';
    b.num = s2n(op+1);
    b.denom = s2n(slash_b+1);



  // Handle operator
  /*** HW2: add your code here ***/
    if(temp_op == '+')
    {
        c = add(a, b);
    }
    else if(temp_op == '-')
    {
        c = sub(a, b);
    }
    else if(temp_op == '*')
    {
        c = mul(a, b);
    }
    printf("%d/%d", c.num, c.denom);

    return 0;
}
