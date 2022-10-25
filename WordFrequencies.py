# -*- coding: utf-8 -*-

import os
import re
import sys

# Read text file and compute word frequencies.
# Output is CSV of word, count, relative_frequency

class frequency():
  def __init__(self, filepath):
    self.f = open(filepath, encoding="utf-8")
    self.count_map = {}
    self.word_count = 0
    self.lowerCase = True
    self.reSplit = re.compile("\W+")
    
  def compute_map(self):
    for line in self.f:
#      words = line.split()
      words = self.reSplit.split(line)
      for word in words:
        if self.lowerCase:
          word = word.lower()
        word = word.strip()  # Remove
        if not word:
          continue
        if word not in self.count_map:
          self.count_map[word] = 1
        else:
          self.count_map[word] += 1
      self.word_count += 1

  def output_frequencies(self):
    keys = self.count_map.keys()
    total = float(self.word_count)
    for word in sorted(keys):
      count = self.count_map[word]
      outline = (word, count, count / total)
      print(outline)

  def sort2(a, b):
    if a[1] == b[1]:
      # Consider alpha if same frequency
      if a[0] < b[0]:
        return 1
      else:
        return -1
    # Frequencies only
    return b[1] - a[1]
  
  def output_tsv(self):
    keys = self.count_map.keys()
    total = float(self.word_count)
    alpha_list = sorted(self.count_map.items(), key=lambda item: item[0])
    for result in sorted(alpha_list, key=lambda item: item[1], reverse=True):
      outline = "%s\t%s" % (result[0], result[1])
      print(outline)

def main(args):
  if len(args) < 2:
    return
  compute = frequency(args[1])
  compute.compute_map()
  #compute.output_frequencies()
  compute.output_tsv()

if __name__ == "__main__":
  main(sys.argv)
