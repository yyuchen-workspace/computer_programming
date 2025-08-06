//最大堆/最小堆 (用陣列實作，1-based index 常見)
int heap[100], size = 0;

void push(int val) {
    int i = ++size;
    while (i > 1 && val > heap[i/2]) {
        heap[i] = heap[i/2];
        i /= 2;
    }
    heap[i] = val;
}

int pop() { // max heap
    int max = heap[1];
    int last = heap[size--], i = 1, child;
    while (i * 2 <= size) {
        child = i * 2;
        if (child < size && heap[child+1] > heap[child]) child++;
        if (last >= heap[child]) break;
        heap[i] = heap[child];
        i = child;
    }
    heap[i] = last;
    return max;
}
