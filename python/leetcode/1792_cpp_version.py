class Solution(object):
    def maxAverageRatio(self, classes, extraStudents):
        """
        :type classes: List[List[int]]
        :type extraStudents: int
        :rtype: float
        """
        n = len(classes)
        res = 0.0
        
        # 實現最大堆 - Python中使用負值來實現最大堆
        pq = []
        for i in range(n):
            gain = (1.0 * classes[i][1] - classes[i][0]) / (1.0 * classes[i][1] * (classes[i][1] + 1))
            pq.append((-gain, i))  # 使用負值實現最大堆
        
        # 對堆進行初始化排序
        pq.sort()
        
        while extraStudents:
            # 找到並移除最大增益
            max_idx = 0
            for j in range(len(pq)):
                if pq[j][0] < pq[max_idx][0]:
                    max_idx = j
            
            neg_gain, idx = pq.pop(max_idx)
            
            # 更新班級
            classes[idx][0] += 1
            classes[idx][1] += 1
            
            # 重新計算增益並加回堆
            new_gain = (1.0 * classes[idx][1] - classes[idx][0]) / (1.0 * classes[idx][1] * (classes[idx][1] + 1))
            pq.append((-new_gain, idx))
            
            extraStudents -= 1
        
        # 計算最終平均值
        for i in range(n):
            res += (1.0 * classes[i][0] / classes[i][1])
        
        return res / n


if __name__ == "__main__":
    solution = Solution()
    
    # Test case 1
    result1 = solution.maxAverageRatio([[1,2],[3,5],[2,2]], 2)
    print(f"Test 1: {result1:.5f}")  # Expected: 0.78333
    
    # Test case 2
    result2 = solution.maxAverageRatio([[2,4],[3,9],[4,5],[2,10]], 4)
    print(f"Test 2: {result2:.5f}")  # Expected: 0.53485