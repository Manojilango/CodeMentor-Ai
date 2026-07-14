class Node:
    def __init__(self, val):
        self.value=val
        self.next=None

def traverse(head):
    current=head
    while current:
        print(current.value)
        current = current.next

node1= Node(10)
node2= Node(20)
node3=Node(30)


node1.next = node2
node2.next = node3


head= node1
traverse(head)