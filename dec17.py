"""--- Day 17: Spinlock ---

Suddenly, whirling in the distance, you notice what looks like a massive,
pixelated hurricane: a deadly spinlock. This spinlock isn't just consuming
computing power, but memory, too; vast, digital mountains are being ripped
from the ground and consumed by the vortex.

If you don't move quickly, fixing that printer will be the least of your
problems.

This spinlock's algorithm is simple but efficient, quickly consuming
everything in its path. It starts with a circular buffer containing only the
value 0, which it marks as the current position. It then steps forward through
the circular buffer some number of steps (your puzzle input) before inserting
the first new value, 1, after the value it stopped on. The inserted value
becomes the current position. Then, it steps forward from there the same
number of steps, and wherever it stops, inserts after it the second new value,
2, and uses that as the new current position again.

It repeats this process of stepping forward, inserting a new value, and using
the location of the inserted value as the new current position a total of 2017
times, inserting 2017 as its final operation, and ending with a total of 2018
values (including 0) in the circular buffer.

For example, if the spinlock were to step 3 times per insert, the circular
buffer would begin to evolve like this (using parentheses to mark the current
position after each iteration of the algorithm):

    (0), the initial state before any insertions.

    0 (1): the spinlock steps forward three times (0, 0, 0), and then inserts
    the first value, 1, after it. 1 becomes the current position.

    0 (2) 1: the spinlock steps forward three times (0, 1, 0), and then
    inserts the second value, 2, after it. 2 becomes the current position.

    0  2 (3) 1: the spinlock steps forward three times (1, 0, 2), and then
    inserts the third value, 3, after it. 3 becomes the current position.

And so on:

    0  2 (4) 3  1
    0 (5) 2  4  3  1
    0  5  2  4  3 (6) 1
    0  5 (7) 2  4  3  6  1
    0  5  7  2  4  3 (8) 6  1
    0 (9) 5  7  2  4  3  8  6  1

Eventually, after 2017 insertions, the section of the circular buffer near the
last insertion looks like this:

1512  1134  151 (2017) 638  1513  851

Perhaps, if you can identify the value that will ultimately be after the last
value written (2017), you can short-circuit the spinlock. In this example,
that would be 638.

What is the value after 2017 in your completed circular buffer?

Your puzzle answer was 1282.


--- Part Two ---

The spinlock does not short-circuit. Instead, it gets more angry. At least,
you assume that's what happened; it's spinning significantly faster than it
was a moment ago.

You have good news and bad news.

The good news is that you have improved calculations for how to stop the
spinlock. They indicate that you actually need to identify the value after 0
in the current state of the circular buffer.

The bad news is that while you were determining this, the spinlock has just
finished inserting its fifty millionth value (50000000).

What is the value after 0 the moment 50000000 is inserted?

Your puzzle answer was 27650600.

"""



#the two options are to store the spinlock as an array or as a linked list

#if it's stored as an array, we can jump ahead once by the given amount in
#constant time but inserting is O(the current len of the lock, which will
#eventually be 2017) - so in total it's approx .5 * 2017^2

#if it's stored as a linked list, inserting is constant but jumping ahead once
#by the given amount is O(that amount), which is this case is 335 - so in total
#it's approx 335 * 2017

#a circular linked list it is!


JUMP_DIST = 335

#this turns out to be overkill, but might as well keep it just as a snippet
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
    return current.next.val


def short_circuit_spin_lock_2():
    """Try again to short circuit the spin lock, this time by finding the value
    immediately after 0."""

    #we'll represent our circular array as a circular linked list, which will
    #have only one node to start, whose value is 0
    current = SLLNode("0")
    current.next = current #to make it circular

    #since we'll need to find it later, keep a pointer to the 0 node
    zero_node = current

    #insert each number in turn, up to 50,000,000
    for new_num in range(1, 50000001):

        if new_num % 1000 == 0:
            print new_num

        #jump forward the requisite amount
        for _ in range(JUMP_DIST):
            current = current.next

        #insert the next number
        current.insert_after(new_num)

        #make the just-inserted number the current location
        current = current.next

    #now that we've inserted all the numbers, find and return the number after
    #0
    return zero_node.next.val



print short_circuit_spin_lock()
from datetime import datetime
begin = datetime.now()
print short_circuit_spin_lock_2()
print datetime.now() - begin



