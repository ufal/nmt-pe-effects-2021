#!/usr/bin/env python3

import argparse
import json
import glob, os
from pathlib import Path
import xmltodict
import re
import sacrebleu
from nltk.tokenize import word_tokenize
from utils import f1

class MxLine():
    def __init__(self, root):
        self.root = root
        self.source = root['trans-unit']['source']
        self.target = root['trans-unit']['target']
        self.tunit_id = root['trans-unit']['@id']

        # the following three fields are set incorrectly, it's up to the caller to define the
        # correct values
        self.comments = []
        self.is_first = False
        self.is_last = False
        
        if self.source[0] == '#':
            self.index = int(re.search('\d+', self.source).group(0))
            return
        
        self.index = None
        self.provided = root['trans-unit']['alt-trans'][1]['target']
        if self.provided is None:
            self.provided = self.source

        self.edit_time = int(root['trans-unit']['m:editing-stats']['m:editing-time'])/1000
        self.think_time = int(root['trans-unit']['m:editing-stats']['m:thinking-time'])/1000
        
        tokens = self.source.split()
        self.edit_time_word = self.edit_time / len(tokens)
        self.think_time_word = self.think_time / len(tokens)

    def chrf(self):
        return sacrebleu.sentence_chrf(self.target, [self.provided]).score

    def ter(self):
        return sacrebleu.sentence_ter(self.target, [self.provided]).score

    def unigram(self):        
        provided_set = word_tokenize(self.provided.lower())
        target_set = word_tokenize(self.target.lower())
        return f1(
            len([x for x in target_set if x in provided_set]) / len(target_set),
            len([x for x in target_set if x in provided_set]) / len(provided_set)
        )

    def clone(self):
        return MxLine(self.root)
        
class MxDoc():
    def __init__(self, lines, user, index, job_uid):
        self.lines = lines
        self.user_u = user
        self.user_a = index['annotator']
        self.doc_name = index['doc_name']
        self.mt_name = index['mt_name']
        self.index = index
        self.job_uid = job_uid
    
    def source(self):
        return ''.join([line.source + '\n' for line in self.lines])

    def provided(self):
        return ''.join([line.provided + '\n' for line in self.lines])

    def target(self):
        return ''.join([line.target + '\n' for line in self.lines])

    def clone(self):
        return MxDoc([x.clone() for x in self.lines], self.user_u, self.index)

    def mut_provided_to_target(self):
        for line in self.lines:
            line.target = line.provided

def parse_lines(lines, user, index_data, job_uid):
    lines = [MxLine(l) for l in lines if 'trans-unit' in l]
    buffer = []
    data = []
    index = None
    for line in lines:
        if line.index is not None:
            if buffer:
                data.append(MxDoc(buffer, user, index, job_uid))
                buffer = []
            index = index_data[str(line.index)]
        else:
            buffer.append(line)
    if buffer:
        data.append(MxDoc(buffer, user, index, job_uid))
    return data

def load_mx():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--mxliff-data-dir', default='docs/memsource/raw-translations')
    parser.add_argument('-i', '--index', default='docs/out_p1/index.json')
    args = parser.parse_known_args()[0]

    with open(args.index, 'r') as f:
        index_data = json.loads(f.read())

    data_files = glob.glob(f'{args.mxliff_data_dir}/*.mxliff')
    data = []
    for fname in data_files:
        with open(fname, 'r') as f:
            tree = xmltodict.parse(f.read())['xliff']
            job_uid = tree['file']['@m:job-uid']
            data += parse_lines(
                tree['file']['body']['group'],
                tree['m:extra']['m:users']['m:user']['@username'],
                index_data,
                job_uid
            )
    return data

if __name__ == '__main__':
    load_mx()