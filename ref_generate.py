import re

ref_file = "BiTeX.txt"
title_mark = False

initials_table_cn = ["b", "p", "m", "f", "d", "t", "n", "l",
                     "g", "k", "h", "j", "q", "x", "zh",
                     "ch", "sh", "r", "z", "c", "s", "y", "w"]

vowel_table_cn = ["a", "o", "e", "i", "u", "v", "ai", "ei",
                  "ui", "ao", "ou", "iu", "ie", "ve", "er", "an",
                  "en", "in", "un", "vn", "ang", "eng", "ing", "ong"]


def fname_split(fname):
    if '-' in fname:  # For the case of Chen, Chia-Chih
        return fname.split('-')

    # zh ch sh
    if fname[0].lower() not in ["z", "c", "s"] or fname[1] != 'h':
        fname_words = [fname[0]]
        jump = 1
    else:
        fname_words = [fname[:2]]
        jump = 2

    for i in range(0, len(fname)):
        if len(fname_words) > 3:
            return [fname]

        if jump > 0:
            jump -= 1
            continue

        if fname[i] in vowel_table_cn:
            if i <= (len(fname) - 1) - 2:
                if fname[i:i + 3] in vowel_table_cn:
                    jump = 2
                    fname_words[-1] += fname[i:i + 3]
                elif fname[i:i + 2] in vowel_table_cn:
                    jump = 1
                    fname_words[-1] += fname[i:i + 2]
                else:
                    fname_words[-1] += fname[i]
            elif i == (len(fname) - 1) - 1:
                if fname[i:i + 2] in vowel_table_cn:
                    jump = 1
                    fname_words[-1] += fname[i:i + 2]
                else:
                    fname_words[-1] += fname[i]
            else:
                fname_words[-1] += fname[i]
        elif fname[i:i + 2] in initials_table_cn:  # zh, ch, sh
            jump = 1
            fname_words.append(fname[i].upper())
            fname_words[-1] += fname[i + 1]
        elif fname[i:i + 1] in initials_table_cn:
            fname_words.append(fname[i].upper())
        else:
            print("Unknow:", fname[i])

    #print(fname_words)
    return fname_words


with open(ref_file, "r") as f:
    text = f.readlines()

with open("lastname_cn.txt", "r") as f:   # Common Chinese last names
    last_name_cn = f.readlines()
    for i in range(len(last_name_cn)):
        last_name_cn[i] = last_name_cn[i][0].upper() + last_name_cn[i][1:]
        last_name_cn[i] = last_name_cn[i].replace("\n", "")
        last_name_cn[i] = last_name_cn[i].replace(" ", "")

ref_list = []
ref_num = 0
for line in text:
    if '@' in line:
        ref_list.append({})
        ref_list[ref_num]['index'] = re.findall(r'\{(.*?),', line)[0]
        ref_num += 1
    elif 'title={' in line and 'booktitle={' not in line:
        ref_list[ref_num-1]['title'] = re.findall(r'\{(.*?)\}', line)[0]
    elif 'author={' in line:
        ref_list[ref_num-1]['author'] = re.findall(r'\{(.*?)\},', line)[0]
    elif 'year={' in line:
        ref_list[ref_num-1]['year'] = re.findall(r'\{(.*?)\}', line)[0]
    elif 'journal={' in line or 'booktitle={' in line:
        ref_list[ref_num-1]['resource'] = re.findall(r'\{(.*?)\}', line)[0]
    elif 'eprint={' in line:
        ref_list[ref_num-1]['resource'] = "arXiv:" + re.findall(r'\{(.*?)\}', line)[0]
    elif 'volume={' in line:
        ref_list[ref_num-1]['volume'] = re.findall(r'\{(.*?)\}', line)[0]
    elif 'number={' in line:
        ref_list[ref_num-1]['number'] = re.findall(r'\{(.*?)\}', line)[0]
    elif 'pages={' in line or 'page={' in line:
        ref_list[ref_num-1]['page'] = re.findall(r'\{(.*?)\}', line)[0]
        if "--" in ref_list[ref_num-1]['page']:
            ref_list[ref_num - 1]['page'] = ref_list[ref_num - 1]['page'].replace("--", "-")

# author, title, resource, volume, number, pages, year.
with open("ref_bib.txt", "w+") as f:
    for item in ref_list:
        f.write("\\bibitem{%s}"%item['index'])
        print(item)

        # author
        for name in item['author'].split('and'):
            name_words = name.split(', ')
            if len(name_words) == 2:
                fname, lname = name_words
                if fname[0] == ' ':
                    fname = fname[1:]

                if lname[-1] == ' ':
                    lname = lname[:-1]

                if lname in last_name_cn:    # CN Name
                    fname_words = fname_split(fname)
                    if len(fname_words) == 2:
                        f.write("%s. %s. %s" % (fname_words[0][0], fname_words[1][0], lname))
                    else:
                        f.write("%s. %s" % (fname_words[0][0], lname))

                elif fname in last_name_cn:    # CN Name, First and last names reversed
                    fname_words = fname_split(lname)
                    if len(fname_words) == 2:
                        f.write("%s. %s. %s" % (fname_words[0][0], fname_words[1][0], fname))
                    else:
                        f.write("%s. %s" % (fname_words[0][0], fname))

                else:
                    # print("%s. %s" % (fname[0], lname))
                    f.write("%s. %s" % (fname[0], lname))
            else:
                f.write(name)
            f.write(', ')

        # title
        if title_mark:
            f.write('"%s"' % item['title'])
        else:
            f.write('%s' % item['title'])
        f.write(', ')

        # resource
        if '&' in item['resource']:
            item['resource'] = item['resource'].replace('&', r'\&')
        f.write(item['resource'])
        f.write(', ')

        # volume
        if 'volume' in item.keys():
            f.write('Vol.%s' % item['volume'])
            f.write(', ')

        # number
        if 'number' in item.keys():
            f.write('No.%s' % item['number'])
            f.write(', ')

        # page
        if 'page' in item.keys():
            f.write('%s' % item['page'])
            f.write(', ')

        # year
        f.write(item['year'])
        f.write(".\n\n")

#print(ref_list)
print("Read references:", ref_num)
