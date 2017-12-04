"""--- Day 4: High-Entropy Passphrases ---

A new system policy has been put in place that requires all accounts to use a
passphrase instead of simply a password. A passphrase consists of a series of
words (lowercase letters) separated by spaces.

To ensure security, a valid passphrase must contain no duplicate words.

For example:

    aa bb cc dd ee is valid.

    aa bb cc dd aa is not valid - the word aa appears more than once.

    aa bb cc dd aaa is valid - aa and aaa count as different words.

The system's full passphrase list is available as your puzzle input. How many
passphrases are valid?

Your puzzle answer was 383.


--- Part Two ---

For added security, yet another system policy has been put in place. Now, a
valid passphrase must contain no two words that are anagrams of each other -
that is, a passphrase is invalid if any word's letters can be rearranged to
form any other word in the passphrase.

For example:

    abcde fghij is a valid passphrase.

    abcde xyz ecdab is not valid - the letters from the third word can be
    rearranged to form the first word.

    a ab abc abd abf abj is a valid passphrase, because all letters need to be
    used when forming another word.

    iiii oiii ooii oooi oooo is valid.

    oiii ioii iioi iiio is not valid - any of these words can be rearranged to
    form any other word.

Under this new system policy, how many passphrases are valid?

Your puzzle answer was 265.

"""


def count_valid_passphrases1(filepath):
    """Count the number of valid passphrases (that is, passphrases with no
       repeated words)."""

    count = 0

    with open(filepath) as passphrase_file:
        for passphrase in passphrase_file:
            words = passphrase.split()

            #sets eliminate duplicates, so if the set is the same size as the
            #list, there were no duplicates and the passphrase is valid
            if len(words) == len(set(words)):
                count += 1

    return count


def count_valid_passphrases2(filepath):
    """Count the number of valid passphrases (that is, passphrases with no
       repeated or anagrammed words)."""


    count = 0

    with open(filepath) as passphrase_file:
        for passphrase in passphrase_file:
            words = passphrase.split()

            #sorting the letters of a word makes anagrams equal each other,
            #so then we can do the same set calculation as in part 1
            sorted_words = ["".join(sorted(word)) for word in words]

            if len(sorted_words) == len(set(sorted_words)):
                count += 1

    return count




print count_valid_passphrases1("dec4.txt")
print count_valid_passphrases2("dec4.txt")
