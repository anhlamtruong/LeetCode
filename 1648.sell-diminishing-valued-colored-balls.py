#
# @lc app=leetcode id=1648 lang=python3
#
# [1648] Sell Diminishing-Valued Colored Balls
#

# @lc code=start
class Solution:
    def maxProfit(self, inventory: List[int], orders: int) -> int:
        """
        [1,2,7,11] order 6
        Sort the inventory
        Use all of the color 11 until the price is down to 7 ? 
        """

        inventory.sort(reverse=True)
        def is_valid(mid):
            count = orders
            for item in inventory:
                if item <= mid:
                    return True
                count -= (item-mid)
                if count < 0:
                    return False 
            return True
        high = max(inventory)
        low = 0
        price = high
        while high >= low:
            mid = (high+low) // 2
            if is_valid(mid):
                price = mid
                high = mid - 1
            else:
                low = mid + 1
        res = 0
        for item in inventory:
            if item > price:
                balls = item - price
                res += balls*(item+price+1)//2
                orders -= balls
            else:
                break
        if orders > 0:
            res += orders*price
        return res % (10**9 + 7)
# @lc code=end

