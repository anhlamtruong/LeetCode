#
# @lc app=leetcode id=847 lang=python3
#
# [847] Shortest Path Visiting All Nodes
#

# @lc code=start
from collections import deque
from typing import List


class Solution:
    def shortestPathLength(self, graph: List[List[int]]) -> int:
        n = len(graph)
        
        if n == 1:
            return 0
        
        final_mask = (1<<n) -1
        
        q = deque()
        
        visited = set()
        
        for i in range(n):
            mask = 1 << i
            q.append((i, mask, 0))
            visited.add((i,mask))
        
        while q:
            node, curr_mask, distance = q.popleft()
            for nei in graph[node]:
                next_mask = curr_mask | (1 << nei)
                
                if next_mask == final_mask:
                    return distance+1
                
                if (nei, next_mask) not in visited:
                    visited.add((nei, next_mask))
                    q.append((nei, next_mask, distance +1))
        return 0
# @lc code=end