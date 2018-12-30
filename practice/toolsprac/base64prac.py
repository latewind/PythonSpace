import base64

if __name__ == '__main__':

    f1 = open("D:/Test/AA.mp3", 'r')

    f2 = open("D:/Test/BB.mp3", 'wb')

    base64.decode(f1, f2)

    a = 1
    if a not in [1, 2, 3]:
        print("NO")
