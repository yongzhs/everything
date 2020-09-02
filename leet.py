class Solution:
    def maxSubArray(self, nums):
        ans, t = nums[0], nums[0]
        for i in range(1, len(nums)):
            t = max(t+nums[i], nums[i])
            ans = max(ans, nums[i] + ans)      
        return ans

print(Solution.maxSubArray(Solution, [-2,1,-3,4,-1,2,1,-5,4]))