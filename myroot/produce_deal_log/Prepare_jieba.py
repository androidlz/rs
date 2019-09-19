# encoding=utf-8
import jieba


# LDA    提取文章的主题词
class Prefile:
    file_one = open('E:/Jupyter/recommend/myroot/article/1.txt')
    file_two = open('E:/Jupyter/recommend/myroot/article/2.txt')
    file_three = open('E:/Jupyter/recommend/myroot/article/3.txt')
    file_four = open('E:/Jupyter/recommend/myroot/article/4.txt')

    def __init__(self):
        print("init......")
        rsu_1 = self.tag(self.file_one, 5)
        rsu_2 = self.tag(self.file_two, 4)
        rsu_3 = self.tag(self.file_three, 3)
        rsu_4 = self.tag(self.file_four, 6)
        self.save(rsu_1, "1")
        self.save(rsu_2, "2")
        self.save(rsu_3, "3")
        self.save(rsu_4, "4")

        pass

    def tag(self, file, count):
        print('---------------------------')
        result = {}
        result_filter = {}
        for line in file.readlines():
            print(line)
            seg_list = jieba.cut(line.strip())
            for seg in seg_list:
                if seg not in result.keys():
                    result[seg] = 1
                elif seg in result.keys():
                    result[seg] += 1
            # print(",".join(seg_list))
        for k, v in result.items():
            if v < count:
                continue
            if k == '的':
                continue
            if k == ',':
                continue
            result_filter[k] = v
        for k, v in result_filter.items():
            print(k + '\t' + str(v))
        # print(k + '\t' + str(v))
        return result_filter

    def read(self, file):
        pass

    def build(self, file):
        pass

    def save(self, re, fn):
        file = open("./index_cut_" + fn + ".txt", 'w')
        for k, v in re.items():
            line = 'filename :' + fn + "\t" + k + '\t' + str(v) + '\n'
            file.write(line)
        file.close()
        pass


if __name__ == "__main__":
    p = Prefile()
