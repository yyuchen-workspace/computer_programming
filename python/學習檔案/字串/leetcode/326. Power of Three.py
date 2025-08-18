class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):        
        
        
        merge_list = nums1+nums2 # 結合串列
        merge_list.sort() #串列大到小排序
        
        list_length = len(merge_list)
        mid_index =  list_length // 2 # 整數除法，無條件捨去小數點
        if list_length % 2 == 1:
            return merge_list[mid_index]
        else:
            return (merge_list[mid_index-1] + merge_list[mid_index]) / 2.0 # python2必須用浮點數運算答案才會是浮點數，python3則無論如何答案都是浮點數
    

if __name__ == "__main__":
    try:
        '''
        nums1 = input("請輸入數列1:")
        list1 = list(map(int, nums1.split()))

        nums2 = input("請輸入數列2:")
        list2 = list(map(int, nums2.split()))
        '''

        # 在此處模擬測試案例的輸入
        list1 = [1, 3]
        list2 = [2]

        median_solution = Solution()
        median = median_solution.findMedianSortedArrays(list1, list2)
        
        print("中位數為: {}".format(median))
    except ValueError:
        print("輸入錯誤！")