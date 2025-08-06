#include<stdio.h>
#include<string.h>
#include<stdint.h>
int main()
{
  uint32_t n1;
  uint32_t n2;
  uint32_t sum;
  printf("Please enter the first number: ");
  scanf("%u", &n1);
  printf("Please enter the second number: ");
  scanf("%u", &n2);
  int array1[10] = {0};
  int array2[10] = {0};
  int array_sum[10] = {0};
  int total1 = 0;
  int total2 = 0;
  int total_sum = 0;
  int dash = 0;
  int arr1_size = sizeof(array1) / sizeof(int);
  int arr2_size = sizeof(array2) / sizeof(int);
  int arr_sum_size = sizeof(array_sum) / sizeof(int);
  sum = n1 * n2;
  int num1 = n1;
  int num2 = n2;
  while(n1 > 0)
  {
    array1[total1] = n1 % 10; //store value in array1
    n1 /= 10; //delete the value of array1[total]
    total1++; //calculate the number of digits in n1
  }


  while(n2 > 0)
  {
    array2[total2] = n2 % 10; //store value in array2
    n2 /= 10; //delete the value of array2[total]
    total2++; //calculate the number of digits in n2
  }

   while(sum >0)
  {
    array_sum[total_sum] = sum % 10; //store value in array_sum
    sum /= 10; //delete the value of array[total_sum]
    total_sum++; //calculate the number of digits in sum
  }

  for(int i = 0 ; i < (total_sum - total1) * 2 + 2; i++)//print space
  {
    printf(" ");
  }

  for (int i = total1 - 1 ; i >= 0 ; i--)//print n1
  {
    printf("%d ", array1[i]);
  }

  printf("\n");
  printf("*)");

  for(int i = 0 ; i < (total_sum - total2) * 2 ; i++)//print space
  {
    printf(" ");
  }

  for (int i = total2 -1 ; i >= 0 ; i--)//print n2
  {
    printf("%d ", array2[i]);

  }

  printf("\n");
  for(int i = 0 ; i < total_sum * 2 + 1 ; i++)//print ---
  {
    printf("-");
  }
  printf("\n");
  
  int distribute[10][20] = {0};
  for (int i = 0; i < total2; i++)
  {
    int carry = 0;
    for (int j = 0; j < total1; j++) 
    {
      int product = array2[i] * array1[j] + carry;
      distribute[i][i + j] = product % 10;
      carry = product / 10;
    }
    distribute[i][i + total1] = carry; // 存储进位

    // 打印部分积
    for (int k = (total_sum - total1 - i) * 2; k > 0; k--)
    {
      printf(" "); // 打印前导空格
    }
    for (int j = total1; j >= 0; j--) 
    {
      if(distribute[i][i + j] == 0 && distribute[i][i + j -1] != 0)
      {  
        printf("  ");
      }
      else if(distribute[i][i + j] == 0 && distribute[i][i + j + 1] == 0)
      {
        for(int quantity = total1 ; quantity > 0 ; quantity--)
        {
          printf("0 ");
          break;
        }
      }
      else
      {
        printf("%d ", distribute[i][i + j]);
      }
    }
      printf("\n");
    }

  for(int i = 0 ; i < total_sum * 2 + 1 ; i++)//print ---
  {
    printf("-");
  }

  printf("\n");
  printf(" ");
  printf(" ");

  for(int i = total_sum - 1 ; i >= 0 ; i--)//print sum
  {

    printf("%d ", array_sum[i]);

  }
}
