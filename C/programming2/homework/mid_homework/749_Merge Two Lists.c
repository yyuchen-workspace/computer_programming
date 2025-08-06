#include <stdio.h>
#include <stdlib.h>

typedef struct _Node {
    int value;
    struct _Node *next;
} Node;

// The function has been obfuscated to prevent you to know what it does.
Node * createList(int whats_dis_idk_plz_dont_touch){
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


int main() {
  int seed1, seed2;
  scanf(&quot;%d %d&quot;, &amp;seed1, &amp;seed2);

  Node *list1 = createList(seed1);
  Node *list2 = createList(seed2);
  Node *pointerToFinalLinkedList = (Node*)malloc(sizeof(Node));
  Node *cur = pointerToFinalLinkedList;

  // rest of your answer
}


