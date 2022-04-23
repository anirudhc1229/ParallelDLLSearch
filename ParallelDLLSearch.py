import multiprocessing
import sys
import time

class Node:
    def __init__(self, next=None, prev=None, data=None):
        self.next = next
        self.prev = prev
        self.data = data

class DoublyLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def push_front(self, new_data):
        self.length += 1
        new_node = Node(data=new_data)
        new_node.next = self.head
        new_node.prev = None
        if self.head is not None:
            self.head.prev = new_node
            return
        self.head = new_node
        self.tail = new_node

    def push_back(self, new_data):
        self.length += 1
        new_node = Node(data=new_data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node

    def search_seq(self, goal):
        start = time.time()
        cur = self.head
        i = 0
        while cur:
            if cur.data == goal:
                end = time.time()
                print(f'sequential search time: {end - start}')
                return i
            cur = cur.next
            i += 1   
        return -1

    def search_par(self, goal):

        mgr = multiprocessing.Manager()
        sys.setrecursionlimit(50000)
        mgr_idx = mgr.Value('i', -1)
        mgr_found = mgr.Value('b', False)
        lock = mgr.Lock()

        fwd_proc = multiprocessing.Process(target=self._search_fwd, args=(goal, mgr_idx, mgr_found, lock))
        rev_proc = multiprocessing.Process(target=self._search_rev, args=(goal, mgr_idx, mgr_found, lock))

        fwd_proc.start()
        rev_proc.start()

        fwd_proc.join()
        rev_proc.join()

        return mgr_idx.value

    def _search_fwd(self, goal, mgr_idx, mgr_found, lock):
        cur = self.head
        i = 0
        while cur and not mgr_found.value:
            if cur.data == goal:
                mgr_found.value = True
                with lock:
                    mgr_idx.value = i
            cur = cur.next
            i += 1

    def _search_rev(self, goal, mgr_idx, mgr_found, lock):
        cur = self.tail
        i = self.length - 1
        while cur and not mgr_found.value:
            if cur.data == goal:
                mgr_found.value = True
                with lock:
                    mgr_idx.value = i
            cur = cur.prev
            i -= 1

    def print_fwd(self):
        cur = self.head
        while cur.next:
            print(f'{cur.data} -> ', end='')
            cur = cur.next
        print(cur.data)

    def print_rev(self):
        cur = self.tail
        while cur.prev:
            print(f'{cur.data} -> ', end='')
            cur = cur.prev
        print(cur.data)

if __name__ == '__main__':
    dll = DoublyLinkedList()
    for num in range(1000):
        dll.push_back(num)
    dll.print_fwd()
    print(dll.search_par(2600))
