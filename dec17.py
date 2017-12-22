
#the two options are to store the spinlock as an array or as a linked list

#if it's stored as an array, we can jump ahead once by the given amount in
#constant time but inserting is O(the current len of the lock, which will
#eventually be 2017) - so in total it's approx .5 * 2017^2

#if it's stored as a linked list, inserting is constant but jumping ahead once
#by the given amount is O(that amount), which is this case is 335 - so in total
#it's approx 335 * 2017

#a circular linked list it is!


JUMP_DIST = 335

class DLLNode(object):
    """A doubly-linked list node."""

    def __init__(self, value):
        self.val = value
        self.prev = None
        self.next = None

    def __repr__(self):
        """Provide helpful representation when printing"""

        repr_str = "<Node {val} prev={prev_val} next={next_val}>"
        return repr_str.format(val=self.val,
                               prev_val=self.prev.val if self.prev else None,
                               next_val=self.next.val if self.next else None)

    def insert_after(self, value):
        """Insert a Node with the given value immediately after this Node."""

        #imagine that we're inserting b between a (self) and c (self.next)

        #grab a and c, and create b
        a = self
        c = self.next
        b = DLLNode(value)

        #note that a is self so definitely exists, b exists because we create
        #it, but c might be None
        a.next = b
        b.prev = a
        b.next = c
        if c:
            c.prev = b


class SLLNode(object):
    """A singly-linked list node."""

    def __init__(self, value):
        self.val = value
        self.next = None

    def __repr__(self):
        """Provide helpful representation when printing"""

        repr_str = "<Node {val} next={next_val}>"
        return repr_str.format(val=self.val,
                               next_val=self.next.val if self.next else None)

    def insert_after(self, value):
        """Insert a Node with the given value immediately after this Node."""

        #imagine that we're inserting b between a (self) and c (self.next)

        #grab a and c, and create b
        a = self
        c = self.next
        b = SLLNode(value)

        #point the pointers
        a.next = b
        b.next = c




def short_circuit_spin_lock():
    """Short circuit the spin lock by determining the value immediately after
    the final inserted value."""

    #we'll represent our circular array as a circular linked list, which will
    #have only one node to start, whose value is 0
    current = SLLNode("0")
    current.next = current #to make it circular

    #insert each number in turn, up to 2017
    for new_num in range(1, 2018):

        #jump forward the requisite amount
        for _ in range(JUMP_DIST):
            current = current.next

        #insert the next number
        current.insert_after(new_num)

        #make the just-inserted number the current location
        current = current.next

    #now that we've inserted all the numbers, find and return the number after
    #2017
    # print current
    return current.next.val


print short_circuit_spin_lock()



