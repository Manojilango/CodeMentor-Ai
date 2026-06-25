class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None

class Solution:
    def mergeTwoLists(self, l1, l2):
        # Step 1 - dummy node
        dummy = ListNode(0)
        current = dummy

        # Step 2+3 - compare and merge
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1  # take from l1
                l1 = l1.next       # move l1 forward
            else:
                current.next = l2  # take from l2
                l2 = l2.next       # move l2 forward
            current = current.next # move current forward

        # Step 4 - attach remaining
        current.next = l1 or l2

        return dummy.next

# Test
def make_list(vals):
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next

def print_list(head):
    vals = []
    while head:
        vals.append(str(head.val))
        head = head.next
    print(" → ".join(vals))

l1 = make_list([1,2,4])
l2 = make_list([1,3,4])

sol = Solution()
result = sol.mergeTwoLists(l1, l2)
print_list(result)  # 1 → 1 → 2 → 3 → 4 → 4