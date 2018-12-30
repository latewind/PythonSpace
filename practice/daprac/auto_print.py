import os
import re


def auto_print(file_path):
    # I don't like add the print statement to the py file
    # but I hope to print the var value
    # so add the print statement auto
    # only support the var which named obj
    source = ""
    with open(file_path) as s:
        for line in s.readlines():
            source = source + line
            if line.strip(' ').startswith("obj ="):
                source = source + '\n'.join(re.findall(r'^\s+', line)) + 'print(obj)\n'
    print(source)
    exec(source)


if __name__ == '__main__':
    auto_print(os.path.abspath('pandas_prac.py'))