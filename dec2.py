"""--- Day 2: Corruption Checksum ---

As you walk through the door, a glowing humanoid shape yells in your
direction. "You there! Your state appears to be idle. Come help us repair the
corruption in this spreadsheet - if we take another millisecond, we'll have to
display an hourglass cursor!"

The spreadsheet consists of rows of apparently-random numbers. To make sure
the recovery process is on the right track, they need you to calculate the
spreadsheet's checksum. For each row, determine the difference between the
largest value and the smallest value; the checksum is the sum of all of these
differences.

For example, given the following spreadsheet:

5 1 9 5
7 5 3
2 4 6 8

    The first row's largest and smallest values are 9 and 1, and their
    difference is 8.

    The second row's largest and smallest values are 7 and 3, and their
    difference is 4.

    The third row's difference is 6.

In this example, the spreadsheet's checksum would be 8 + 4 + 6 = 18.

What is the checksum for the spreadsheet in your puzzle input?

Your puzzle answer was 36174.

--- Part Two ---

"Great work; looks like we're on the right track after all. Here's a star for
your effort." However, the program seems a little worried. Can programs be
worried?

"Based on what we're seeing, it looks like all the User wanted is some
information about the evenly divisible values in the spreadsheet.
Unfortunately, none of us are equipped for that kind of calculation - most of
us specialize in bitwise operations."

It sounds like the goal is to find the only two numbers in each row where one
evenly divides the other - that is, where the result of the division operation
is a whole number. They would like you to find those numbers on each line,
divide them, and add up each line's result.

For example, given the following spreadsheet:

5 9 2 8
9 4 7 3
3 8 6 5

    In the first row, the only two numbers that evenly divide are 8 and 2; the
    result of this division is 4.

    In the second row, the two numbers are 9 and 3; the result is 3.

    In the third row, the result is 2.

In this example, the sum of the results would be 4 + 3 + 2 = 9.

What is the sum of each row's result in your puzzle input?

Your puzzle answer was 244."""


from itertools import product

def find_min_max_checksum(matrix_str):
    """Given a string representing a matrix of numbers, find the checksum (the
       sum of the ranges (max - min) for each row)."""

    #create an actual matrix out of the matrix string
    matrix = [[int(num) for num in row.split()]
              for row in matrix_str.split("\n")]

    total_checksum = 0

    #loop over the matrix, row by row, computing the checksum for each and
    #adding it to the total
    for row in matrix:
        row_checksum = max(row) - min(row)
        total_checksum += row_checksum

    return total_checksum


def find_divisible_pair_quotient(row):
    """Given a row (list) of numbers, find the pair where one divides the other
       and return their quotient."""

    #loop over the cartesian product of the list with itself, checking if each
    #pair qualifies
    #note that this will lead to us checking entries against themselves, so
    #weed those out
    for a, b in product(row, row):
        if a != b and a % b == 0:
            #if we've found a pair that works, return the quotient
            return a / b


def find_divisibility_checksum(matrix_str):
    """Given a string representing a matrix of numbers, find the divisibility
       checksum (the sum of the quotients of the one pair of numbers in each
       row in which one evenly divides the other)."""

    #create an actual matrix out of the matrix string
    matrix = [[int(num) for num in row.split()]
              for row in matrix_str.split("\n")]

    total_checksum = 0

    #loop over the matrix, row by row, computing the checksum for each and
    #adding it to the total
    for row in matrix:
        row_checksum = find_divisible_pair_quotient(row)
        total_checksum += row_checksum

    return total_checksum


print find_min_max_checksum("""3751  3769  2769  2039  2794  240   3579  1228  4291  220   324   3960  211   1346  237   1586
550   589   538   110   167   567   99    203   524   288   500   111   118   185   505   74
2127  1904  199   221   1201  250   1119  377   1633  1801  2011  1794  394   238   206   680
435   1703  1385  1461  213   1211  192   1553  1580  197   571   195   326   1491  869   1282
109   104   3033  120   652   2752  1822  2518  1289  1053  1397  951   3015  3016  125   1782
2025  1920  1891  99    1057  1909  2237  106   97    920   603   1841  2150  1980  1970  88
1870  170   167   176   306   1909  1825  1709  168   1400  359   817   1678  1718  1594  1552
98    81    216   677   572   295   38    574   403   74    91    534   662   588   511   51
453   1153  666   695   63    69    68    58    524   1088  75    1117  1192  1232  1046  443
3893  441   1825  3730  3660  115   4503  4105  3495  4092  48    3852  132   156   150   4229
867   44    571   40    884   922   418   328   901   845   42    860   932   53    432   569
905   717   162   4536  4219  179   990   374   4409  4821  393   4181  4054  4958  186   193
2610  2936  218   2552  3281  761   204   3433  3699  2727  3065  3624  193   926   1866  236
2602  216   495   3733  183   4688  2893  4042  3066  3810  189   4392  3900  4321  2814  159
166   136   80    185   135   78    177   123   82    150   121   145   115   63    68    24
214   221   265   766   959   1038  226   1188  1122  117   458   1105  1285  1017  274   281""")

print find_divisibility_checksum("""3751  3769  2769  2039  2794  240   3579  1228  4291  220   324   3960  211   1346  237   1586
550   589   538   110   167   567   99    203   524   288   500   111   118   185   505   74
2127  1904  199   221   1201  250   1119  377   1633  1801  2011  1794  394   238   206   680
435   1703  1385  1461  213   1211  192   1553  1580  197   571   195   326   1491  869   1282
109   104   3033  120   652   2752  1822  2518  1289  1053  1397  951   3015  3016  125   1782
2025  1920  1891  99    1057  1909  2237  106   97    920   603   1841  2150  1980  1970  88
1870  170   167   176   306   1909  1825  1709  168   1400  359   817   1678  1718  1594  1552
98    81    216   677   572   295   38    574   403   74    91    534   662   588   511   51
453   1153  666   695   63    69    68    58    524   1088  75    1117  1192  1232  1046  443
3893  441   1825  3730  3660  115   4503  4105  3495  4092  48    3852  132   156   150   4229
867   44    571   40    884   922   418   328   901   845   42    860   932   53    432   569
905   717   162   4536  4219  179   990   374   4409  4821  393   4181  4054  4958  186   193
2610  2936  218   2552  3281  761   204   3433  3699  2727  3065  3624  193   926   1866  236
2602  216   495   3733  183   4688  2893  4042  3066  3810  189   4392  3900  4321  2814  159
166   136   80    185   135   78    177   123   82    150   121   145   115   63    68    24
214   221   265   766   959   1038  226   1188  1122  117   458   1105  1285  1017  274   281""")
