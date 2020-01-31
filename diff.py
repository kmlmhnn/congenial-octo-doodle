#!/usr/bin/env python3

import sys
import argparse
from collections import Counter


class Differ:
    def __init__(self, f1, f2, fout):
        self.f1 = f1
        self.f2 = f2
        self.fout = fout
        self.lines_common = self.count_lines(f1) & self.count_lines(f2)

    @staticmethod
    def count_lines(file):
        line_count = Counter()
        for line in file:
            l = line.rstrip()
            line_count[l] += 1
        return line_count

    def print_f1_and_f2(self):
        self.f1.seek(0, 0)
        line_count = self.lines_common.copy()
        for line in self.f1:
            l = line.rstrip()
            if line_count[l]:
                line_count[l] -= 1
                print(line, end="", file=self.fout)

    def print_f1_minus_f2(self):
        self.print_difference_wrt(self.f1)

    def print_f2_minus_f1(self):
        self.print_difference_wrt(self.f2)

    def print_difference_wrt(self, file):
        file.seek(0, 0)
        line_count = self.lines_common.copy()
        for line in file:
            l = line.rstrip()
            if line_count[l]:
                line_count[l] -= 1
            else:
                print(line, end="", file=self.fout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", type=argparse.FileType("r"))
    parser.add_argument("file2", type=argparse.FileType("r"))
    args = parser.parse_args()

    d = Differ(args.file1, args.file2, sys.stdout)
    d.print_f1_and_f2()
    print("---")
    d.print_f1_minus_f2()
    print("---")
    d.print_f2_minus_f1()
