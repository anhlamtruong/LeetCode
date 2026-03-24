#
# @lc app=leetcode id=1284 lang=python3
#
# [1284] Minimum Number of Flips to Convert Binary Matrix to Zero Matrix
#

# @lc code=start
class Solution:
    def minFlips(self, mat: List[List[int]]) -> int:
        R,C = len(mat), len(mat[0])
        if R == C == 1:
            return 0 if mat[0][0] == 0 else 1

        init_state = 0
        q = deque()
        visit= set()
        directions = [[0,0],[0,1], [1,0], [-1,0], [0,-1]]
        #convert 2d matrix to bitwise
        for r in range(R):
            for c in range(C):
                k = r*C+c
                if mat[r][c]:
                    init_state = init_state | (1<<k)
        flip_mask = []
        for r in range(R):
            for c in range(C):
                mask = 0
                for dr, dc in directions:
                    nr,nc = dr+r, dc+c
                    if min(nr,nc) < 0 or nr == R or nc == C:
                        continue
                    k = nr * C + nc
                    mask |= (1 << k)
                flip_mask.append(mask)
        q.append((init_state, 0))
        visit.add(init_state)
        while q:
            state, curr_steps = q.popleft()
            if state == 0:
                return curr_steps
            for mask in flip_mask:
                new_state = state ^ mask
                if new_state in visit:
                    continue
                q.append((new_state, curr_steps+ 1))
                visit.add(new_state)

        return -1 
# @lc code=end

