//支援 int、或回傳 char[]


// 把整數轉為二進位字串（buf 需至少 33 字元長，含 '\0'）
void int_to_binary_str(int num, char *buf) {
    for (int i = 31; i >= 0; i--) {
        buf[31 - i] = ((num >> i) & 1) ? '1' : '0';
    }
    buf[32] = '\0';  // 字串結尾
}
