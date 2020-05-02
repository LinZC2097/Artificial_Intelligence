import jieba


def word_frequency(file_addr: str) -> dict:
    excludes = {"什么", "一个", "我们", "那里", "你们", "如今", \
                "说道", "知道", "老太太", "起来", "姑娘", \
                "这里", "出来", "他们", "众人", "自己", "一面", \
                "太太", "只见", "怎么", "奶奶", "两个", "没有", \
                "不是", "不知", "这个", "听见"}
    includes = {"宝玉", "贾母", "凤姐", "王夫人", "贾琏", "平儿", \
                "袭人", "宝钗", "黛玉", "薛姨妈", "探春", "鸳鸯", "贾政", \
                "晴雯", "湘云", "刘姥姥", "邢夫人", "贾珍", "紫鹃", "香菱", \
                "尤氏", "薛蟠", "贾赦", "周瑞家", "贾芸", "贾蓉", "林之孝", "雨村", "迎春", "赵姨娘"}
    f = open(file_addr, "r", encoding="gb18030")
    txt = f.read()
    f.close()
    words = jieba.lcut(txt)
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1

    del_list = []
    for word in counts.keys():
        if word not in includes:
            del_list.append(word)
    for word in del_list:
        del (counts[word])

    # for word in excludes:
    #     if word in counts:
    #         del (counts[word])

    # items = list(counts.items())
    # items.sort(key=lambda x: x[1], reverse=True)
    # for i in range(5):
    #     word, count = items[i]
    #     # print("{0: < 10}{1: > 5}".format(word, count))
    #     print(word,"\t",count)
    return counts


def main():
    print("hello world")
    top_num = 50
    most_frequent = []
    chapter = [[] for _ in range(top_num)]
    chapter_freq = []
    hongloumeng_add = "/Users/marsscho/PycharmProjects/Artificial_Intelligence/hongloumeng.txt"

    all_word = word_frequency(hongloumeng_add)
    all_word = list(all_word.items())
    all_word.sort(key=lambda x: x[1], reverse=True)
    top_word = all_word[:top_num]
    # for i in range(len(top_word)):
    #     word, count = top_word[i]
    #     # print("{0: < 10}{1: > 5}".format(word, count))
    #     print(word, "\t", count, "\t", chapter[i])

    chapter_add = "/Users/marsscho/PycharmProjects/Artificial_Intelligence/hongloumeng/hongloumeng_chapter"

    for i in range(120):
        chapter_freq.append(word_frequency(chapter_add + str(i + 1) + ".txt"))

    for i in range(len(top_word)):
        word, index = top_word[i]
        for j in range(120):
            if word in chapter_freq[j]:
                chapter[i].append(j + 1)

    print("name", "\t", "frequency", "\t", "chapter")
    for i in range(len(top_word)):
        word, count = top_word[i]
        print(word, "\t", count, "\t\t", chapter[i])


if __name__ == '__main__':
    main()
