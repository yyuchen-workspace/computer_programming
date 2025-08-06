void print_twos_complement_info(unsigned char num) {
    unsigned char ones_comp = ~num;
    unsigned char twos_comp = ones_comp + 1;
    signed char signed_result = (signed char)twos_comp;

}
