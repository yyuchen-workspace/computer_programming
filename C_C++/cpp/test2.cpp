#include<stdio.h>
int main()
{
    int a;
    int b = 0;
    int c = 117;
    printf("Please enter the password...>");
    scanf("%d", &a);
    while(a != c && b < 4)
    {
        printf("Wrong password.Input again...>");
        scanf("%d", &a);
        b++;
    }
    if(a != 117)
    {
        printf("Your account is locked.Please e-mail to the administrator.");
        
    }
    else
    {
        printf("Great! The program starts.\n");

    }    
    

}