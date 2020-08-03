# -*- coding:utf-8 -*-

"""
此脚本负责统计语料的总体情况
打乱数据以及划分数据集
"""

import os
import re
from random import shuffle


class TrainDataViewer(object):

    def __init__(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            self.data = f.read()
        with open(file_path, "r", encoding="utf-8") as f:
            self.line_data = f.readlines()
        self.tags = set()

    def main(self, only_shuffle=False, cut_data=False):
        self.count_all()
        self.count_every_type()
        if only_shuffle:
            self.shuffle()
        if cut_data:
            self.cut_data_set()

    def count_all(self):
        """
        统计语料总数
        :return:
        """
        cut = self.data.split("\n\n")
        count_all = 0
        for i in cut:
            if i == "" or i == "\n" or i == "\n\n":
                continue
            count_all += 1
        print("此数据集共有句子：", count_all)

    def count_every_type(self):
        """
        统计各类实体的情况
        :return:
        """
        information = dict()
        for line in self.line_data:
            match_result = re.search("(?<=B-|I-)(.*?)(?=\n|$)", line)
            if match_result is not None:
                tag = match_result.group()
                self.tags.add(tag)

                if "B-" in line:
                    if tag not in information:
                        information[tag] = 0
                    information[tag] += 1
        print("各槽位统计：", str(information))

    def shuffle(self):
        # 只打乱不切割
        if os.path.exists("_train.txt"):
            os.remove("_train.txt")
        output_filename = "_train.txt"
        train_write_file = open(output_filename, "a", encoding="utf-8")
        cut = self.data.split("\n\n")
        shuffle(cut)
        for i in cut:
            train_write_file.write(i.strip("\n").strip())
            train_write_file.write("\n\n")

    def cut_data_set(self):
        if os.path.exists("data.txt"):
            os.remove("data.txt")
        if os.path.exists("test.txt"):
            os.remove("test.txt")
        # 测试集占多少比例
        ratio = 0.1
        train_set_filename = "data.txt"
        test_set_filename = "test.txt"

        train_write_file = open(train_set_filename, "a", encoding="utf-8")
        test_write_file = open(test_set_filename, "a", encoding="utf-8")
        cut = self.data.split("\n\n")
        offset = int(len(cut) * (1-ratio))
        shuffle(cut)
        train_set = cut[:offset]
        test_set = cut[offset:]
        for i in train_set:
            train_write_file.write(i.strip("\n").strip())
            train_write_file.write("\n\n")
        for j in test_set:
            test_write_file.write(j.strip("\n").strip())
            test_write_file.write("\n\n")
        train_write_file.close()
        test_write_file.close()


if __name__ == "__main__":
    TrainDataViewer("data.txt").main(cut_data=True)
