#!/usr/bin/env python3

# merge data from both phases into a single JSON file with correct usernames for all stages

from load import *
import json
import sys

data_phase_1 = load_mx(p1_only=True)

lines = {}
m11_outputs = {}
ref_outputs = {}

for doc in data_phase_1:
    for line in doc.lines:
        line_key = f"{doc.mt_name},{doc.doc_name},{doc.user_a},{line.source}"

        lines[line_key] = {
            "mt_name": doc.mt_name,
            "doc_name": doc.doc_name,
            "username_phase_1": doc.user_u,
            "source": line.source,
            "provided": line.provided,
            "target_after_phase_1": line.target,
        }

        if doc.mt_name == 'm11':
            m11_outputs[f"{doc.doc_name},{line.source}"] = line.provided
        elif doc.mt_name == 'ref':
            ref_outputs[f"{doc.doc_name},{line.source}"] = line.provided

# hack to feed the load_mx, so that we get data from second phase
sys.argv.extend(
    ["-d", "docs/memsource/revisions/", "-i", "docs/out_p2/index-consistent-names.json"]
)

data_phase_2 = load_mx(p1_only=True)

for doc in data_phase_2:
    for line in doc.lines:
        line.source = line.source.replace("{1}", "{j}")
        line_key = f"{doc.mt_name},{doc.doc_name},{doc.user_a},{line.source}"

        try:
            line_record = lines[line_key]

            print(json.dumps({
                "username_phase_2": doc.user_u,
                "target_after_phase_2": line.target,
                **line_record
            }, ensure_ascii=False))
        except KeyError:
            if doc.user_a == 'rm':
                fake_target_phase_1 = m11_outputs[f"{doc.doc_name},{line.source}"]
            elif doc.user_a == 'rr':
                fake_target_phase_1 = ref_outputs[f"{doc.doc_name},{line.source}"]
            else:
                raise Exception(f"unexpected missing key {line_key}")

            print(json.dumps({
                "mt_name": doc.mt_name,
                "doc_name": doc.doc_name,
                "username_phase_1": f"FAKE_{doc.user_a}",
                "source": line.source,
                "provided": "",
                "target_after_phase_1": fake_target_phase_1,
                "username_phase_2": doc.user_u,
                "target_after_phase_2": line.target,
            }, ensure_ascii=False))
