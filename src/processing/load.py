#!/usr/bin/env python3

import argparse
import json
import glob, os
from pathlib import Path
import xmltodict
import re

class MxLine():
    def __init__(self, root):
        self.source = root['trans-unit']['source']
        self.target = root['trans-unit']['target']
        
        if self.source[0] == '#':
            self.index = int(re.search('\d+', self.source).group(0))
            return
        
        self.index = None
        self.provided = root['trans-unit']['alt-trans'][1]['target']
        if self.provided is None:
            self.provided = self.source

        self.edit_time = int(root['trans-unit']['m:editing-stats']['m:editing-time'])/1000
        self.think_time = int(root['trans-unit']['m:editing-stats']['m:thinking-time'])/1000
        
        tokens = self.provided.split()
        self.edit_time_word = self.edit_time / len(tokens)
        self.think_time_word = self.think_time / len(tokens)

    def clone_shallow(self):
        return self
        
class MxDoc():
    def __init__(self, lines, user, index):
        self.lines = lines
        self.user_u = user
        self.user_a = index['annotator']
        self.doc_name = index['doc_name']
        self.mt_name = index['mt_name']
        self.index = index
    
    def source(self):
        return ''.join([line.source + '\n' for line in self.lines])

    def provided(self):
        return ''.join([line.provided + '\n' for line in self.lines])

    def target(self):
        return ''.join([line.target + '\n' for line in self.lines])

    def clone_shallow(self):
        return MxDoc([x.clone_shallow() for x in self.lines], self.user_u, self.index)

    def mut_provided_to_target(self):
        for line in self.lines:
            line.target = line.provided

def parse_lines(lines, user, index_data):
    lines = [MxLine(l) for l in lines if 'trans-unit' in l]
    buffer = []
    data = []
    index = None
    for line in lines:
        if line.index is not None:
            if buffer:
                data.append(MxDoc(buffer, user, index))
                buffer = []
            index = index_data[str(line.index)]
        else:
            buffer.append(line)
    if buffer:
        data.append(MxDoc(buffer, user, index))
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
            data += parse_lines(
                tree['file']['body']['group'],
                tree['m:extra']['m:users']['m:user']['@username'],
                index_data
            )
    return data

if __name__ == '__main__':
    load_mx()