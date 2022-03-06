import os, re, pypinyin

char_list = r'「」“”（）()'

num_list_1 = '零一二三四五六七八九'
num_list_2 = '十百千万十百千亿十百千万'

# def cheak_conversation(text):
#     for chars in char_list:
#         if chars in text:
#             return True
#         else:
#             pass
#     return False

def cheak_repeat(input):
    for i in input:
        repeat_num = input.count(i)
        if repeat_num > (len(input)*0.5) or i in '呃啊嗯阿啦哇呀哦噢喔嘿哎呵哼哈' or not u'\u4e00' <= i <= u'\u9fff': # 'a' <= i <= 'z' or 'A' <= i <= 'Z' or u'\uFF0C' < i < u'\uFF5A':
            return False
        else:
            continue
    return True

def num_to_chinese(text):
    while re.search(r'\d', text):
        exchange_text = ''
        num_range = re.search(r'\d+', text).span()
        org_num = text[num_range[0]:num_range[1]]
        if re.search(r'\d+号', text):
            for i in org_num:
                exchange_text += num_list_1[int(i)]
            text = re.sub(org_num, exchange_text, text, 1)
            continue
        elif re.search(r'\d+', text):
            if len(org_num) > 13:
                return 'ERROR_agsrae'
            else:
                for i in range(0,len(org_num)):
                    exchange_text += num_list_1[int(org_num[i])]
                    if int(len(org_num))-i-2 >= 0:
                        exchange_text += num_list_2[int(len(org_num))-i-2]
                    else:
                        pass
                text = re.sub(org_num, exchange_text, text, 1)
            continue 
    return text
            

os.chdir(os.path.dirname(__file__))

file_list = os.listdir()

output_file = open("aidatatang_200_zh_transcript.txt",mode='w+', encoding='utf-8')

for file_name in file_list:
    if os.path.splitext(file_name)[1] != '.txt' or file_name == 'aidatatang_200_zh_transcript.txt':
        continue
    else:
        line_title = ''
        for i in file_name[:-4]:
            if u'\u4e00' <= i <= u'\u9fff':
                line_title += pypinyin.pinyin(i, pypinyin.Style.NORMAL)[0][0][0].upper()
            elif i.isnumeric():
                line_title += i 
            else:
                line_title += ''
        line_title = re.sub('\W','_',line_title)
        num_counter = 0
        input_file = open(file_name, mode='r' ,encoding='utf-8')
        file_date = input_file.readlines()
        output_line = []
        for text_date in file_date:
            if text_date.strip() == '':
                continue
            else:
                text_date = text_date.strip()
                text_split =  re.split(r'\W', text_date) #之前是「|」|“|”|（|）|’|‘|。|！|？
                i = 0
                for splited_date in text_split:
                    buffer_1 = splited_date
                    splited_date = num_to_chinese(splited_date)
                    if splited_date == 'ERROR_agsrae':
                        text_split.remove(buffer_1)
                        continue
                    else:
                        text_split[text_split.index(buffer_1)] = splited_date
                    i += 1
                    if len(splited_date) >= 300:
                        splited_date = re.split('，', splited_date)
                        for date_insert in splited_date:
                            text_split.insert(i, date_insert)
                            i += 1
                for splited_date in text_split:
                    if len(re.sub('\W','',splited_date)) < 6:
                        continue
                    elif cheak_repeat(re.sub('\W','',splited_date)):
                        output_line.append(line_title + '_' + str(num_counter) + ' ' + re.sub('\W', ' ', splited_date) + '\n')
                        # output_line.append(re.sub('\W', '', splited_date)+"\n")
                        num_counter += 1
                    else:
                        pass
        input_file.close()
        output_file.writelines(output_line)
        output_file.flush()
    
output_file.close()
                

