class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """


nums1 = input("請輸入數列1:")
nums1_splited = nums1.split()
list1 = list(map(int, nums1_splited))

nums2 = input("請輸入數列2:")
nums2_splited = nums2.split() 
list2 = list(map(int, nums2_splited))
list1.extend(list2)
list1.sort()

mid_index = len(list1) // 2
if mid_index % 2 == 1:
    median = list1[mid_index]
else:
    median = (list1[mid_index-1] + list1[mid_index-2]) / 2

print(f"中位數為{median}")