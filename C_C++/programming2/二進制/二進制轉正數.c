unsigned char to_positive(signed char neg) {
    // �p�G�O���ơA�����૬�^��
    if (neg >= 0)
        return (unsigned char)neg;

    // �Y�O�t�ơA�θɽX�޿�ӳB�z�G
    // �p��ϸɽX�G���ϦA�[1���u�Ͼާ@�v�N�O -1 �A����
    return (unsigned char)(~neg + 1);
}
