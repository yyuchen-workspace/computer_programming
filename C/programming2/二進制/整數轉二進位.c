//�䴩 int�B�Φ^�� char[]


// �����ର�G�i��r��]buf �ݦܤ� 33 �r�����A�t '\0'�^
void int_to_binary_str(int num, char *buf) {
    for (int i = 31; i >= 0; i--) {
        buf[31 - i] = ((num >> i) & 1) ? '1' : '0';
    }
    buf[32] = '\0';  // �r�굲��
}
