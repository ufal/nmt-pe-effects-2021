"""Transform a parallel corpus into a translation memory file (TMX)."""

import sys
import argparse
import xml.etree.ElementTree as ET
from typing import Iterator, Tuple


def make_tunit_variant(lang: str, text: str, tunit: ET.Element):
    ns = "{http://www.w3.org/XML/1998/namespace}"
    tuv = ET.SubElement(tunit, "tuv", attrib={ns + "lang": lang})
    seg = ET.SubElement(tuv, "seg")
    seg.text = text


def create_tmx(segments: Iterator[Tuple[str, str]], src_lang: str, tgt_lang: str) -> ET.Element:
    root = ET.Element("tmx", attrib={"version": "1.4"})
    ET.SubElement(root, "header", attrib={"srclang": src_lang})

    body = ET.SubElement(root, "body")
    for src_line, tgt_line in segments:
        tu = ET.SubElement(body, "tu")
        make_tunit_variant(src_lang, src_line, tu)
        make_tunit_variant(tgt_lang, tgt_line, tu)

    return root


def read_parallel_corpus(src_file: str, tgt_file: str) -> Iterator[Tuple[str, str]]:
    with open(src_file) as src_hdl, open(tgt_file) as tgt_hdl:
        for src_line, tgt_line in zip(src_hdl, tgt_hdl):
            yield src_line.rstrip(), tgt_line.rstrip()


def remove_aux_lines(segments: Iterator[Tuple[str, str]]) -> Iterator[Tuple[str, str]]:
    for src_line, tgt_line in segments:
        if src_line.lstrip().startswith('#') or tgt_line == "! (no translation available)":
            continue
        yield src_line, tgt_line


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("src_file_path", help="file with source sentences")
    parser.add_argument("tgt_file_path", help="file with target sentences")
    parser.add_argument("--src-lang", default="en", help="source text language")
    parser.add_argument("--tgt-lang", default="cs", help="target text language")

    args = parser.parse_args()

    segments = read_parallel_corpus(args.src_file_path, args.tgt_file_path)
    filtered = remove_aux_lines(segments)
    tmx = create_tmx(filtered, args.src_lang, args.tgt_lang)

    sys.stdout.buffer.write(ET.tostring(tmx, encoding='UTF-8'))


if __name__ == '__main__':
    main()
