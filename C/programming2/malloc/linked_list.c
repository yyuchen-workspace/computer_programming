#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int data;
    struct ListNode *next;
} ListNode;

// 印出整條 linked list
void printLinkedList(ListNode *head) {
    while (head != NULL) {
        printf("%d -> ", head->data);
        head = head->next;
    }
    printf("NULL\n");
}

// 釋放 linked list 的記憶體
void freeLinkedList(ListNode *head) {
    while (head != NULL) {
        ListNode *temp = head;
        head = head->next;
        free(temp);
    }
}

int main() {
    ListNode *head = NULL;
    ListNode *tail = NULL;

    // 建立一條包含 0~4 的 linked list
    for (int i = 0; i < 5; i++) {
        ListNode *newNode = (ListNode *)malloc(sizeof(ListNode));
        if (newNode == NULL) {
            perror("malloc failed");
            exit(EXIT_FAILURE);
        }
        newNode->data = i;
        newNode->next = NULL;

        if (head == NULL) {
            head = newNode;
            tail = newNode;
        } else {
            tail->next = newNode;
            tail = newNode;
        }
    }

    // 印出鏈結串列
    printf("Linked List: ");
    printLinkedList(head);

    // 釋放記憶體
    freeLinkedList(head);

    return 0;
}
