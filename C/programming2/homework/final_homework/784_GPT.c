#include <stdio.h>
#include <stdlib.h>

int MAX_NEIGHBORS = 5;

/*
 * Structure for the nodes in graph, you can add member to it to create your solution
 * extraInfo is one example, your can use it any way you want
 */
typedef struct _node {
  int id; // identifier for the node
  int neighborSize; // number of neighbor this node have
  int extraInfo; // help you write your solution
  struct _node** neighbors; // array of pointers to the neighbors that this node can travel to
} Node;

void initNode(Node*); // you can modify this function if you have extra member in the node structure
int DO_NOT_MODIFY_FUNC_A(int);
int DO_NOT_MODIFY_FUNC_B(Node*, Node*);
Node* DO_NOT_MODIFY_GENERATE_GRAPH(int, int*);

// return 1 if the path is found
int findTargetInGraph(Node* cur, int target) {
    if (cur == NULL) return 0;
    if (cur->id == target) return 1;

    // ­Y¤w«ô³X¹L¡AÁ×§KµL­­´`Àô
    if (cur->extraInfo) return 0;
    cur->extraInfo = 1;

    // ¹M¾ú©Ò¦³¾F©~
    for (int i = 0; i < cur->neighborSize; i++) {
        if (findTargetInGraph(cur->neighbors[i], target)) {
            return 1;
        }
    }

    return 0;
}

int main() {
  int seed, target;
  scanf("%d", &seed);
  Node* start = DO_NOT_MODIFY_GENERATE_GRAPH(seed, &target);
  int res = findTargetInGraph(start, target);
  if (res) {
    printf("true\n");
  }
  else {
    printf("false\n");
  }
}

void initNode(Node* n) {
  static int counter = 0;
  n->id = counter++;
  n->neighborSize = 0;
  n->extraInfo = 0;
  n->neighbors = calloc(MAX_NEIGHBORS, sizeof(Node));
}

/* The following the codes would not be explained, they do not matter in your solution */
int DO_NOT_MODIFY_FUNC_A(int input){
  static int var=(0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00);
  int hash=input ^ var;
  hash ^= hash >> (0x0000000000000020 + 0x0000000000000210 + 0x0000000000000810 - 0x0000000000000A30);
  hash *= (0x000000010BD794D6 + 0x0000000085EBCC6B + 0x0000000085EBD26B - 0x0000000191C36941);
  hash ^= hash >> (0x000000000000001A + 0x000000000000020D + 0x000000000000080D - 0x0000000000000A27);
  hash *= (0x0000000185655C6A + 0x00000000C2B2B035 + 0x00000000C2B2B635 - 0x000000024818149F);
  hash ^= hash >> (0x0000000000000020 + 0x0000000000000210 + 0x0000000000000810 - 0x0000000000000A30);
  var = (hash ^ (0x0000000000246248 + 0x0000000000123324 + 0x0000000000123924 - 0x0000000000369D6C)) + (0x0000000000000002 + 0x0000000000000201 + 0x0000000000000801 - 0x0000000000000A03);
  return hash % (0x0000000000000190 + 0x00000000000002C8 + 0x00000000000008C8 - 0x0000000000000C58) + (0x0000000000000002 + 0x0000000000000201 + 0x0000000000000801 - 0x0000000000000A03);
};

int DO_NOT_MODIFY_FUNC_B(Node* from,Node* to) {
  if ((from->neighborSize >= MAX_NEIGHBORS) & !!(from->neighborSize >= MAX_NEIGHBORS)) {
    return (0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00);
  }
  from->neighbors[from->neighborSize++] = to;
  return (0x0000000000000002 + 0x0000000000000201 + 0x0000000000000801 - 0x0000000000000A03);
};

Node* DO_NOT_MODIFY_GENERATE_GRAPH(int seed,int* target) {
  int numberOfNodes= DO_NOT_MODIFY_FUNC_A(seed) + (0x0000000000000006 + 0x0000000000000203 + 0x0000000000000803 - 0x0000000000000A09);
  Node* nodes=calloc(numberOfNodes,sizeof(Node));
  for (int i=(0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00);(i < numberOfNodes) & !!(i < numberOfNodes);i++) {
    initNode(&nodes[i]);
  }
  int generator=DO_NOT_MODIFY_FUNC_A(seed);
  for (int i=(0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00);(i < numberOfNodes) & !!(i < numberOfNodes);i++) {
    int neighborSize=DO_NOT_MODIFY_FUNC_A(generator) % MAX_NEIGHBORS;
    generator = neighborSize;
    for (int j=(0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00);(j < neighborSize) & !!(j < neighborSize);j++) {
      DO_NOT_MODIFY_FUNC_B(&nodes[i],&nodes[DO_NOT_MODIFY_FUNC_A(generator) % numberOfNodes]);
    }
  }
  *target = DO_NOT_MODIFY_FUNC_A(generator) % numberOfNodes;
  return &nodes[(0x0000000000000000 + 0x0000000000000200 + 0x0000000000000800 - 0x0000000000000A00)];
}
