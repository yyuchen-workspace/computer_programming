#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef struct _Node {
    int val;
    struct _Node* next;
} Node;

Node* create_list(int o_2a98c4abba975e730e5df3a44798e493)
{
    Node* o_755167c30303fdd28d6607e816be72d4 = malloc(sizeof(Node)), * o_6a9434a58009d461a1790617119569f9 = o_755167c30303fdd28d6607e816be72d4;
    int o_6a507c0948c8d7fb82747ad4b8d2f942 = o_2a98c4abba975e730e5df3a44798e493 * o_2a98c4abba975e730e5df3a44798e493;
    while ((o_6a507c0948c8d7fb82747ad4b8d2f942 > (0x000 + 0x200 + 0x800 - 0xA00)) && !!(o_6a507c0948c8d7fb82747ad4b8d2f942 > (0x000 + 0x200 + 0x800 - 0xA00)))
    {
        int o_4c5d13fd0abe657d640631ad80c7dfbe = o_2a98c4abba975e730e5df3a44798e493 * o_6a507c0948c8d7fb82747ad4b8d2f942 * sqrt(o_6a507c0948c8d7fb82747ad4b8d2f942) / (0x0004 + 0x0202 + 0x0802 - 0x0A06);
        o_6a9434a58009d461a1790617119569f9->next = malloc(sizeof(Node));
        o_6a9434a58009d461a1790617119569f9 = o_6a9434a58009d461a1790617119569f9->next;
        o_6a9434a58009d461a1790617119569f9->val = o_4c5d13fd0abe657d640631ad80c7dfbe;
        o_6a9434a58009d461a1790617119569f9->next = NULL;
        o_6a507c0948c8d7fb82747ad4b8d2f942--;
    };
    o_755167c30303fdd28d6607e816be72d4 = o_755167c30303fdd28d6607e816be72d4->next;
    return o_755167c30303fdd28d6607e816be72d4;
}

Node* reverse_list(Node* head) {
    Node *prevNode = NULL, *curNode = head, *nextNode;
    while(curNode != NULL)
    {
         nextNode = curNode->next;//next=B//next=C //NULL
         curNode->next = prevNode;//cur.next(A->next) = NULL //cur.next(B->next) = A //cur.next(C->next) = B
         prevNode = curNode;//pre = A //pre = B //pre = C
         curNode = nextNode;//cur = B //cur = C ////cur = NULL

    }
    return prevNode;
}

int main() {
    int N;
    scanf("%d", &N);
    Node* head = create_list(N);
    Node* reversed_head = reverse_list(head);
    while (reversed_head) {
        printf("%d ", reversed_head->val);
        reversed_head = reversed_head->next;
    }
    return 0;
}









/*🧩 一步一步看過程（以 A → B → C 為例）
初始狀態：
c
複製
編輯
prev = NULL;
cur = A;
next = B;
🔁 第一次迴圈：
c
複製
編輯
cur->next = prev;   // A->next = NULL （反轉方向）
prev = cur;         // prev = A
cur = next;         // cur = B
next = cur->next;   // next = C
此時 List 狀態為：

css
複製
編輯
A → NULL   （已反轉）
B → C      （還沒動）
🔁 第二次迴圈：
c
複製
編輯
cur->next = prev;   // B->next = A
prev = cur;         // prev = B
cur = next;         // cur = C
next = cur->next;   // next = NULL
List 狀態變成：

css
複製
編輯
B → A → NULL   （已反轉）
C              （還沒動）
🔁 第三次迴圈：
c
複製
編輯
cur->next = prev;   // C->next = B
prev = cur;         // prev = C
cur = next;         // cur = NULL（結束）
List 最終變成：

css
複製
編輯
C → B → A → NULL
這就是完全反轉的結果。

🧠 為什麼有效？
因為 Linked List 本質上只是「節點之間的指向關係」，如果你把每個節點的指向反過來，整個鏈的流向自然也就反了。

📌 核心一句話總結：
反轉 Linked List，其實就是改變每個節點的 next 指標方向。
*/
