# -*- coding:utf-8 -*-


from evaluate import PredictService


class Report(object):

    def __init__(self, file_path):
        self.ps = PredictService()
        self.test_file = file_path
        with open(file_path, "r", encoding="utf-8") as f:
            a = f.read()
        sentences_bio = a.split("\n\n")
        self.sentences = []
        self.tags = []
        for i in sentences_bio:
            if len(i.lstrip("\n").rstrip("\n")) == 0:
                continue
            b = i.split("\n")
            sentence = "".join([i.split(" ")[0] for i in b]).lstrip("\n").rstrip("\n")
            print(sentence)
            tag = []
            for i in b:
                cut_line = i.split(" ")
                if len(cut_line) > 1:
                    tag.append(cut_line[1])

            self.sentences.append(sentence)
            self.tags.append(tag)


    def slots_performance(self):
        chosens = self.get_tags()

        for chosen in chosens:
            print("槽位：", chosen)
            num_correct = 0
            num_proposed = 0
            num_gold = 0
            for _id, sentence in enumerate(self.sentences):
                predict_result = self.ps.predict(sentence)
                for pre_id, pre_tag in enumerate(predict_result[0]):
                    if pre_tag == self.tags[_id][pre_id] and chosen in self.tags[_id][pre_id]:
                        num_correct += 1
                    if chosen in pre_tag:
                        num_proposed += 1
                    if chosen in self.tags[_id][pre_id]:
                        num_gold += 1
            precision = num_correct / num_proposed
            recall = num_correct / num_gold
            print("precision：", precision)
            print("recall：", recall)
            print("F1：", 2 * precision * recall / (precision + recall))



    def cal_total_performance(self):
        num_correct = 0
        num_proposed = 0
        num_gold = 0
        """
        总体性能：
        precision = num_correct / num_proposed
        recall = num_correct / num_gold
        f1 = 2 * precision * recall / (precision + recall)
        """
        for _id, sentence in enumerate(self.sentences):
            right_flag = True
            predict_result = self.ps.predict(sentence)
            for pre_id, pre_tag in enumerate(predict_result[0]):
                if pre_tag == self.tags[_id][pre_id] and self.tags[_id][pre_id] != "O":
                    num_correct += 1
                if pre_tag != self.tags[_id][pre_id]:
                    right_flag = False
                if pre_tag != "O":
                    num_proposed += 1
                if self.tags[_id][pre_id] != "O":
                    num_gold += 1
            if not right_flag:
                print("句子：", sentence)
                print("标注：", self.tags[_id])
                print("预测为：", predict_result[0])
                print("*****************")
        precision = num_correct / num_proposed
        recall = num_correct / num_gold
        print("总体性能precision：", precision)
        print("总体性能recall：", recall)
        print("总体性能F1：", 2 * precision * recall / (precision + recall))


    def get_tags(self):
        tag = set()
        for sentence_tag in self.tags:
            for i in sentence_tag:
                if i == "O":
                    continue
                else:
                    tag.add(i.lstrip("B-").lstrip("I-"))
        return tag


if __name__ == "__main__":
    Report("data/data_gen0610/test.txt").main2()
