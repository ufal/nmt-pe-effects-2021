#!/usr/bin/env python3

import argparse
import json
import glob
import os
from pathlib import Path
import xmltodict
import re
import sacrebleu
from nltk.tokenize import word_tokenize
from collections import defaultdict
from utils import f1


class MxLine():
    def __init__(self, root, spec=False):
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

        self.edit_time = int(
            root['trans-unit']['m:editing-stats']['m:editing-time'])/1000
        self.think_time = int(
            root['trans-unit']['m:editing-stats']['m:thinking-time'])/1000

        tokens = self.source.split()
        self.edit_time_word = self.edit_time / len(tokens)
        self.think_time_word = self.think_time / len(tokens)
    
    def convert_to_template(self):
        del self.target
        del self.tunit_id
        del self.edit_time
        del self.think_time
        del self.edit_time_word
        del self.think_time_word

    def update_rev_line(self, rev_line):
        assert(len(rev_line.keys()) > 0)
        assert(rev_line['revision_provided'] == rev_line['source'])
        self.revision_edit_time = rev_line['revision_edit_time']
        self.revision_edit_time_word = rev_line['revision_edit_time_word']
        self.revision_think_time = rev_line['revision_think_time']
        self.revision_think_time_word = rev_line['revision_think_time_word']
        self.revision_is_first = rev_line['revision_is_first']
        self.revision_is_last = rev_line['revision_is_last']
        self.revision_target = rev_line['target']
        self.lqa = [
            conversation['references']['lqa']
            if 'lqa' in conversation['references']
            else []
            for conversation in rev_line['revision_conversation']
        ]
        self.lqa = [x for x in self.lqa if len(x) != 0]
        self.lqa = [item for subl in self.lqa for item in subl]

    def lqa_count(self):
        return sum([x['severityId'] for x in self.lqa])

    def chrf_p0_p1(self):
        if hasattr(self, "target"):
            return sacrebleu.sentence_chrf(self.target, [self.provided]).score
        else:
            return 0

    def chrf_p1_p2(self):
        if hasattr(self, "target"):
            return sacrebleu.sentence_chrf(self.revision_target, [self.target]).score
        else:
            return 0

    def chrf_p0_p2(self):
        return sacrebleu.sentence_chrf(self.revision_target, [self.provided]).score

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

    def update_rev_doc(self, rev_doc):
        for line in self.lines:
            # tags are changed from {j} to {1}
            line.update_rev_line(rev_doc[line.source.replace("{j}", "{1}")])

    def source(self):
        return ''.join([line.source + '\n' for line in self.lines])

    def provided(self):
        return ''.join([line.provided + '\n' for line in self.lines])

    def target(self):
        return ''.join([line.target + '\n' for line in self.lines])

    def clone(self, spec=False):
        doc = MxDoc([x.clone() for x in self.lines], self.user_u, self.index, self.job_uid)
        if spec:
            [line.convert_to_template() for line in doc.lines]
        return doc

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


def load_mx(p1_only=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--mxliff-data-dir',
                        default='docs/memsource/raw-translations')
    parser.add_argument('-r', '--revisions',
                        default='docs/memsource/data-phase-2.json')
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
    if p1_only:
        return data

    data_templates = {}
    for doc in data:
        if (doc.mt_name, doc.doc_name) not in data_templates:
            data_templates[(doc.mt_name, doc.doc_name)] = doc.clone(spec=True)
    for (mt_name, doc_name), doc in data_templates.items():
        if mt_name == "ref":
            doc.user_a = "rr"
            doc.mt_name += "r"
            data.append(doc)
        elif mt_name == "m11":
            doc.user_a = "rm"
            doc.mt_name += "r"
            data.append(doc)
        else:
            pass

    with open(args.revisions, 'r') as f:
        rev_data = defaultdict(lambda: defaultdict(
            lambda: defaultdict(lambda: defaultdict(lambda: {}))))
        for line in f:
            rev_line = json.loads(line)
            if rev_line['user_a'] in {"rr", "rm"}:
                rev_data[rev_line['doc_name']][rev_line['user_a']][rev_line['mt_name']+"r"][rev_line['source']] = rev_line
            else:
                rev_data[rev_line['doc_name']][rev_line['user_a']][rev_line['mt_name']][rev_line['source']] = rev_line

    # for doc_name in set(rev_data.keys()):
    #     data.append(MxDoc([], -1, {"annotator": -1, "doc_name": doc_name, "mt_name": "ref"}, None))

    for doc in data:
        doc.update_rev_doc(rev_data[doc.doc_name][doc.user_a][doc.mt_name])

    return data


if __name__ == '__main__':
    load_mx()
