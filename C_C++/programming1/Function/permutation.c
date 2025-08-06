void permutation(int num, int num[])
{
        for (int i = 0; i < num; i++)
        {
            for(int j = i + 1; j < num; j++)
            {
                if(num[i] > num[j])
                {
                    
                    int32_t tmp = num[i];
                    num[i] = num[j];
                    num[j] = tmp;
                }
            }
        }
}