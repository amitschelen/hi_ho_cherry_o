# asks for an input in a range
# if input is not an integer in the range, prompt to reenter until range is met
# returns the input
def input_in_range(lower, upper, prompt):
    var = None
    while var not in range(lower, upper):
        try:
            var = int(input(prompt))
            if var < lower or var > upper-1:
                raise ValueError
        except:
            print('Please enter a number from '+str(lower)+' to '+str(upper-1)+'.')
    return var


# asks for a yes/no input
# if the input is not yes or no, prompt to re-enter until yes/no
# returns the input
def input_yes_no(prompt):
    var = None
    while var not in ('yes', 'no'):
        try:
            var = input(prompt)
            if var == 'yes' or var == 'no':
                return var
        except:
            print('Please enter \'yes\' or \'no\' without quotes.')
