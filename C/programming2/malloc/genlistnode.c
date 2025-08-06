#inclde<stdio.h>
#include<stdlib.h>

#define ARRAYSIZE 5

typedef struct list ListNode
{
    int data;
    ListNode *next;

};


void printLinkedList(ListNode *node)
{
   for (; node != NULL; node = node->next)
	printf(¡¨data = %d\n¡¨, node->data);
}


void freeLinkedList(ListNode *node)
{
   while (node != NULL) {
	ListNode *next = node->next;
	free(node);
	node = next;
   }
}


ListNode *genListNode(int data, ListNode *next)
{
   ListNode *node = (ListNode *) malloc(sizeof(ListNode));
   assert(node != NULL);
   node->data = data;
   node->next = next;
    return node;
}


int main()
{
    array[ARRAYSIZE] = {};
    for(int i = 0 ; i < ARRAYSIZE ; i++)
    {
        scanf("%d", &array[i]);
    }


    ListNode *head;
    for(int i = 0 ; i < ARRAYSIZE ; i++)
    {
        *previous = NULL;
        head = genListNode(array[i], previous);
        previous = head;
    }

    printLinkedList(head);
    freeLinkedList(head);
}
