# 未完成

class Solution(object):
    def maxAverageRatio(self, classes, extraStudents):
        """
        :type classes: List[List[int]]
        :type extraStudents: int
        :rtype: float
        """
        
        new_classes = [] #[pass, total, increase]
        for passed, total in classes:
            increase = (passed + 1) / (total + 1) - passed / total
            new_classes.append([passed, total, increase])

        new_classes.sort(key=lambda sub_list: sub_list[2], reverse=True)
        
        '''
        # 測試結構
        count = 0
        for passed, total, _ in new_classes:
            print(f"list{count}: [{passed}, {total}, {_}]")
            count+=1
        '''

        for i in range(extraStudents):
            new_classes[0][0] += 1
            new_classes[0][1] += 1
            new_classes[0][2] = (new_classes[0][0] + 1) / (new_classes[0][1] + 1) - new_classes[0][0] / new_classes[0][1]
            new_classes.sort(key=lambda sub_list: sub_list[2], reverse=True)
            '''
            # 測試結構
            count = 0        
            print(f"LOOP{i}")
            for passed, total, _ in new_classes:
                print(f"list{count}: [{passed}, {total}, {_}]")
                count+=1
            '''  
        
        
        classes_total = 0
        for passed, total, _ in new_classes:
            classes_total += passed / total 
        
        return classes_total / len(new_classes)

            
            
            
    

if __name__ =="__main__":
    solution = Solution()
    average = solution.maxAverageRatio([[2,4],[3,9],[4,5],[2,10]], 4)
    print(average)
