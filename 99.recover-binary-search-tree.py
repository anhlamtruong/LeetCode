#
# @lc app=leetcode id=99 lang=python3
#
# [99] Recover Binary Search Tree
#

# @lc code=start
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        prev = None
        first_mistake= None
        second_mistake =None
        
        def dfs(node):
            nonlocal prev, first_mistake, second_mistake
            if not node:
                return
            
            dfs(node.left)
            #do something 
            if prev and prev.val > node.val:
                if not first_mistake:
                    first_mistake = prev
                    second_mistake = node
                else:
                    second_mistake = node
                    
            prev = node
            dfs(node.right)
        
        dfs(root)
        if first_mistake and second_mistake:
            first_mistake.val, second_mistake.val = second_mistake.val, first_mistake.val
        
# @lc code=end

