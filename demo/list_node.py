class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def PrintListNode(head):
    if head is None:
        print('None')
        return
    result = str(head.val)
    while head.next is not None:
        result += '->'
        result += str(head.next.val)
        head = head.next
    print(result)


def CreateListNone(length):
    if length < 1:
        return None
    i = 1
    result = ListNode(0)
    result_tail = result
    while i < length:
        result_tail.next = ListNode(i)
        result_tail = result_tail.next
        i += 1
    return result


PrintListNode(CreateListNone(10))
