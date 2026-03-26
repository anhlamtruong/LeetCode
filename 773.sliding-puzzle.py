#
# @lc app=leetcode id=773 lang=python3
#
# [773] Sliding Puzzle
#

# @lc code=start
class Solution:
    def slidingPuzzle(self, board: List[List[int]]) -> int:
        final_state = "123450"
        direction = {0:[1,3], 
                    1:[0,2,4], 
                    2:[1,5],
                    3:[0,4],
                    4:[3,1,5],
                    5:[2,4]}
        init_state_list = []
        for r in range(2):
            for c in range(3):
                init_state_list.append(str(board[r][c]))
        init_state = "".join(init_state_list)
        zero_index = init_state.index('0')

        if init_state == final_state:
            return 0
            
        visit = set()
        q = deque()
        q.append((init_state, zero_index, 0))
        visit.add((init_state,zero_index))


        def process_swap(state, index_1, index_2):
            res = list(state)
            res[index_1], res[index_2] = res[index_2], res[index_1]
            return "".join(res) 

        while q:
            for _ in range(len(q)):
                curr_state,z_index, move = q.popleft()
                # print(f"curr_state: {curr_state}")
                for nei in direction[z_index]:
                    # print(f"nei: {nei}")
                    # print(f"z_index: {z_index}\n")
                    new_state = process_swap(curr_state,z_index, nei)
                    if new_state == final_state:
                        return move+1
                    if (new_state,nei) in visit:
                        continue
                    q.append((new_state,nei,move+1))
                    visit.add((new_state,nei))
        return -1
# @lc code=end

