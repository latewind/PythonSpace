import re
import os

dir_path = r'D:\MirServer2\Mir200\Envir\MonItems.old'
for file in os.listdir(dir_path):
    print(file)
    if file.endswith('TXT') or file.endswith('txt'):
        new_lines = ""
        with open(dir_path + "\\" + file, 'r', encoding='gb2312') as f:
            lines = f.readlines()
            print(lines)
            for single_line in lines:
                m = re.match(r'^1/(\d+) (.*)', single_line)
                if m is not None:
                    print(int(m.group(1)))
                    print(m.group(2))
                    i = int(m.group(1))
                    if i > 100:
                        new_lines += "1/" + str(i // 10) + " " + m.group(2) + "\n"
                        continue
                else:
                    pass
                new_lines += single_line

        with open(r"D:\MirServer2\Mir200\Envir\MonItems" + "\\" + file, 'w', encoding='gb2312') as nf:
            nf.writelines(new_lines)
