#include <stdio.h>
#include <stdlib.h>

typedef struct _Node {
    int value;
    struct _Node *next;
} Node;

// The function has been obfuscated to prevent you from knowing what it does.
Node * createList(int whats_dis_idk_plz_dont_touch) {
    Node* something_you_will_use_later = (Node* )malloc(sizeof(Node));
    int idk = (whats_dis_idk_plz_dont_touch % (0x000000000000006A + 0x0000000000000235 + 0x0000000000000835 - 0x0000000000000A9F)) + (0x0000000000000002 + 0x0000000000000201 + 0x0000000000000801 - 0x0000000000000A03);
    something_you_will_use_later->value = (0x0000000000000002 + 0x0000000000000201 + 0x0000000000000801 - 0x0000000000000A03) + (whats_dis_idk_plz_dont_touch % (0x000000000000000E + 0x0000000000000207 + 0x0000000000000807 - 0x0000000000000A15));
    Node* o_391e0e173b58db = something_you_will_use_later;
    int o_054ffc5e91b3c3db6d665a11051c69ad = something_you_will_use_later->value;
    for (int o_6a63317a5a26bb803b098d436705ec13 = (0x0000000000000002 + 0x0000000000000201 + 0x0000000000000801 - 0x0000000000000A03); (o_6a63317a5a26bb803b098d436705ec13 < idk) & !!(o_6a63317a5a26bb803b098d436705ec13 < idk);o_6a63317a5a26bb803b098d436705ec13++) {
        Node* o_fa533b = (Node* )malloc(sizeof(Node));
        o_fa533b->value = o_054ffc5e91b3c3db6d665a11051c69ad + (whats_dis_idk_plz_dont_touch * (0x00000000000000C2 + 0x0000000000000261 + 0x0000000000000861 - 0x0000000000000B23) % (0x00000000000007CA + 0x00000000000005E5 + 0x0000000000000BE5 - 0x00000000000015AF));
        o_391e0e173b58db->next = o_fa533b;
        o_391e0e173b58db = o_fa533b;
        o_054ffc5e91b3c3db6d665a11051c69ad = o_391e0e173b58db->value;
        whats_dis_idk_plz_dont_touch = whats_dis_idk_plz_dont_touch * (0x000000000000004A + 0x0000000000000225 + 0x0000000000000825 - 0x0000000000000A6F) % (0x0000000000005B3A + 0x0000000000002F9D + 0x000000000000359D - 0x00000000000092D7);
    }
    o_391e0e173b58db->next = NULL;
    return something_you_will_use_later;
}

// Function to merge two sorted linked lists
Node* mergeLists(Node* list1, Node* list2) {
    Node* merged = (Node*)malloc(sizeof(Node));
    Node* current = merged;

    while (list1 != NULL && list2 != NULL) {
        if (list1->value <= list2->value) {
            current->next = list1;
            list1 = list1->next;
        } else {
            current->next = list2;
            list2 = list2->next;
        }
        current = current->next;
    }

    // If one list is exhausted, append the other list
    if (list1 != NULL) {
        current->next = list1;
    } else {
        current->next = list2;
    }

    return merged->next;  // Return the merged list without the dummy head
}

// Function to print the linked list
void printList(Node* head) {
    while (head != NULL) {
        printf("%d ", head->value);
        head = head->next;
    }
    printf("\n");
}

int main() {
    int seed1, seed2;
    scanf("%d %d", &seed1, &seed2);

    Node* list1 = createList(seed1);
    Node* list2 = createList(seed2);

    // Merge the two sorted lists
    Node* mergedList = mergeLists(list1, list2);

    // Print the merged list
    printList(mergedList);

    return 0;
}
