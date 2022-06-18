import jieba
import os
import chardet

# TODO: 结合新词构建的词典，进一步加载，
#  input: new_Dicts文件夹下的每个子文件夹（一个子文件夹代表一次迭代，一次迭代以天为单位）下的各个新词典

def check_file_charset(file):
    with open(file,'rb') as f:
        return chardet.detect(f.read())

def convert_to_utf8():
    print("Converting dicts to utf-8 encoding...")
    dict_root_path = "./Dicts"
    if not os.path.exists(os.path.join(dict_root_path, 'sougou.txt')):
        # 用于把搜狗词库转化为utf-8格式
        file_list = os.listdir(dict_root_path)
        f_type = check_file_charset(os.path.join(dict_root_path, file_list[0]))
        fin = open(os.path.join(dict_root_path, file_list[0]),'r', encoding=f_type['encoding'], errors='ignore')
        fout = open(os.path.join(dict_root_path, "sougou.txt"),'w',encoding='utf-8')
        for line in fin:
                fout.write(line)
        fin.close()
        fout.close()
    if not os.path.exists(os.path.join(dict_root_path, 'THUOCL_diming_utf8.txt')):
        f_type = check_file_charset(os.path.join(dict_root_path, 'THUOCL_diming.txt'))
        fin = open(os.path.join(dict_root_path, 'THUOCL_diming.txt'), 'r', encoding=f_type['encoding'], errors='ignore')
        fout = open(os.path.join(dict_root_path, "THUOCL_diming_utf8.txt"), 'w', encoding='utf-8')
        for line in fin:
            fout.write(line)
        fin.close()
        fout.close()
    print("Convert finished!")

# TODO: 加上由分类程序构建出来的新词典
def loadMyDicts():
    dict_root_path = "./Dicts"
    file_list = os.listdir(dict_root_path)
    print("loading user defined dicts...")
    for file in file_list:
        abs_path = os.path.join(dict_root_path, file)
        f_type = check_file_charset(abs_path)
        if f_type['encoding'] == 'utf-8':
            print(file)
            jieba.load_userdict(abs_path)
    print("user defined dicts loaded!")


# 对文件进行分词
def splitFile(inputFile,outputFile):
    fin = open(inputFile,'r',encoding='utf-8')
    fout = open(outputFile,'w',encoding='utf-8')
    for line in fin:
        line = line.strip()
        line = jieba.cut(line) #采用“精确模式进行切词”
        outstr = " ".join(line)
        # print(outstr)
        fout.write(outstr + '\n')
    fin.close()
    fout.close()


def mySplitWords(text_root_path, output_split_words_root_path):
    # text_root_path = "./TXTs/2022年06月01日"
    # output_split_words_root_path = "./output_split_words/2022年06月01日"
    if not os.path.exists(output_split_words_root_path):
        os.makedirs(output_split_words_root_path)
    text_file_list = os.listdir(text_root_path)
    for text_file in text_file_list:
        fr = os.path.join(text_root_path, text_file)
        fw = os.path.join(output_split_words_root_path, text_file)
        splitFile(fr,fw)

# TODO: 输出每次迭代时间，语料多少篇，产生新词数量多少，旧词数量多少
def iteratively_split_words(num_iter = 3):
    text_root_path = "./TXTs"
    output_split_words_root_path = "./TXTs_output_split_words"
    if not os.path.exists(output_split_words_root_path):
        os.makedirs(output_split_words_root_path)
    text_sub_dir_list = os.listdir(text_root_path)
    output_sub_dir_list = os.listdir(output_split_words_root_path)
    st = len(output_sub_dir_list)
    print("splitting words...")
    cnt = 1
    for sub_dir in text_sub_dir_list[st:(st + num_iter)]:
        source_path = os.path.join(text_root_path, sub_dir)
        target_path = os.path.join(output_split_words_root_path, sub_dir)
        print("the %d th iteration: splitting words in %s" % (cnt, source_path))
        mySplitWords(source_path, target_path)
        cnt += 1
    print("split words finished!")

def count_words():
    pass

if __name__ == '__main__':
    convert_to_utf8()
    loadMyDicts()
    iteratively_split_words()# 可以指定迭代次数,由前端输入
