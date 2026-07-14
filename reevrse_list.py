class ListNode:
    def __init__(self, val=0):
        self.val = val
        self.next = None


class Solution:
    def reverseList(self, head):
        prev = None
        curr = head

        while curr:
            next_node = curr.next  # save next
            curr.next = prev       # reverse arrow
            prev = curr            # move prev
            curr = next_node       # move curr

        return prev


def build_list(values):
    head = ListNode(values[0])
    current = head
    for v in values[1:]:
        current.next = ListNode(v)
        current = current.next
    return head


def print_list(head):
    result = []
    while head:
        result.append(head.val)
        head = head.next
    print(result)


sol = Solution()
head = build_list([1, 2, 3, 4, 5])
new_head = sol.reverseList(head)
print_list(new_head)   # expected: [5, 4, 3, 2, 1]