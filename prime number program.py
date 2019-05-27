def prime_number(x):
    print('running prime number check...')
    RANGE = list(range(2, x))
    for option in RANGE:
        while x % option != 0 and option < x:
            option += 1
            continue
        if x % option == 0 and option < x:
            print('This number is not prime')
            break
        else:
            print('This number is prime')
            break


def prime_number_list(a):
    RANGE = list(range(2, a))
    if 2 > num_start:
        print(2)
    for option in RANGE:
        while a % option != 0 and option < a:
            option += 1
            continue
        if a % option == 0 and option < a:
            break
        else:
            print(a)
            break


while True:
    desire = input('To check if a number is prime, type check. \n \
To generate a list of prime numbers, type generate. Hit enter to submit. \n')
    if 'check' in desire.lower():
        x = int(float(input('Enter a number to check: ')))
        prime_number(x)
    elif 'generate' in desire.lower():
        num_start = int(float(input("What number do you want to start at? ")))
        num_end = int(float(input("What number do you want to end at? ")))
        a = list(range(num_start, num_end + 1))
        for nums in a:
            prime_number_list(num_start)
            num_start += 1
    else:
        print('Input error. Try again.')
