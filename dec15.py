
GEN_A_START_VAL = 618
GEN_B_START_VAL = 814


def get_agreement_count(num_trials):
    """Count how many times the least significant 16 bits agree in
       num_trials."""

    count = 0
    prev_val_A = GEN_A_START_VAL
    prev_val_B = GEN_B_START_VAL

    for trial_num in range(num_trials):
        if trial_num % 1000 == 0:
            print trial_num

        #get the next value from each generator
        new_val_A = (prev_val_A * 16807) % 2147483647
        new_val_B = (prev_val_B * 48271) % 2147483647

        #if their least significant 16 bits match, add one to our count
        if bin(new_val_A)[-16:] == bin(new_val_B)[-16:]:
            count += 1

        #move on to the next trial
        prev_val_A = new_val_A
        prev_val_B = new_val_B

    return count


from datetime import datetime
begin = datetime.now()
print get_agreement_count(40000000)
print datetime.now() - begin



