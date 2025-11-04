#
# @lc app=leetcode id=2242 lang=python3
#
# [2242] Maximum Score of a Node Sequence
#

# @lc code=start
from collections import defaultdict
import heapq


class Solution:
    def maximumScore(self, scores: List[int], edges: List[List[int]]) -> int:
        """
        Graph Problem
        Create graph using adj list
        
        Using disktra algo
        """
        adj = defaultdict(list) # (src: [des, weight])
        
        for src,des in edges:
            
            adj[src].append(des)
            adj[des].append(src)
        
        def bfs(init_node):
            max_heap= [] #node, cur_weight
            
            heapq.heappush(max_heap, [-1*scores[init_node], init_node])
            visit = set([init_node])
            count = 3
            while max_heap:
                cur_weight, node = heapq.heappop(max_heap)
                
                
                if count == 0:
                    return -1*cur_weight
                for nei in adj[node]:
                    if nei in visit:
                        continue
                    visit.add(nei)
                    heapq.heappush(max_heap, [-1*(-1*cur_weight+scores[nei]), nei])
                count -= 1
            return -1 
        
        res = -1
        for i in range(len(scores)):
            res = max(res, bfs(i))
        return res
        
            
# @lc code=end

