#include <stdio.h>
#include <stdlib.h>

typedef struct ListNode {
    int data;
    struct ListNode *next;
} ListNode;

// �L�X��� linked list
void printLinkedList(ListNode *head) {
    while (head != NULL) {
        printf("%d -> ", head->data);
        head = head->next;
    }
    printf("NULL\n");
}

// ���� linked list ���O����
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

    // �إߤ@���]�t 0~4 �� linked list
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

    // �L�X�쵲��C
    printf("Linked List: ");
    printLinkedList(head);

    // ����O����
    freeLinkedList(head);

    return 0;
}
