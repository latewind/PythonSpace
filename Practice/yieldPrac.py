import math


def is_prime(number):
    if number > 1:
        if number == 2:
            return True
        if number % 2 == 0:
            return False
        for cur in range(3, int(math.sqrt(number) + 1), 2):
            if number % cur == 0:
                return False
        return True
    return False


if __name__ == '__main__':
    print(is_prime(4))
