unsigned char to_positive(signed char neg) {
    // 如果是正數，直接轉型回傳
    if (neg >= 0)
        return (unsigned char)neg;

    // 若是負數，用補碼邏輯來處理：
    // 計算反補碼：取反再加1的「反操作」就是 -1 再取反
    return (unsigned char)(~neg + 1);
}
