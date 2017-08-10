class EvenOnly(list):
    def append(self, integer):
        if not isinstance(integer, int):
            raise TypeError('Only integers can be added')
        if integer % 2:
            raise ValueError('Only even numbers can be added')
        super().append(integer)

def no_return():
    print('I am about to return an exception.')
    raise Exception('This is always raised.')
    print('This line will never execute.')
    return "I won't be returned"

def call_exceptor():
    print('call_exceptor starts here.')
    no_return()
    print('an exception was raised')
    print("so these lines don't run")
    
try:
    no_return()
except:
    print('Caught an exception')
print('Executed after exception')

def funny_division(divider):
    try:
        return 100 / divider
    except ZeroDivisionError:
        return 'Zero is not a good idea!'
    
print(funny_division(0))
print(funny_division(50.0))
print(funny_division("hello"))

def funny_division2(anumber):
    try:
        if anumber == 13:
            raise ValueError("13 is an unlucky number")
        return 100 / anumber
    except (ZeroDivisionError, TypeError):
        return 'Enter a number other than zero'

for val in (0, "hello", 50.0, 13):
    print("Testing {}:".format(val), end=" ")
    print(funny_division2(val))
    
def funny_division3(anumber):
    try:
        if anumber == 13:
            raise ValueError("13 is an unlucky number")
        return 100 / anumber
    except ZeroDivisionError:
        return 'Enter a number other than zero'
    except TypeError:
        return 'Enter a numerical value'
    except  ValueError:
        print('No, No, not 13!')
        raise # Re-raises exception again