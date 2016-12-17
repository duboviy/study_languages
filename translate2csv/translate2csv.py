#!/usr/bin/env python
import re
import csv
import logging as log
import argparse

import translate


def _get_source_words(source):
    words = set()

    with open(source, 'r') as file:
        for line in file:
            temp_words = re.split('[\W]', line)

            for word in temp_words:
                word = word.lower()

                if word is not None and not word.isdigit() and len(word) > 2:
                    words.add(word)

    return words


def _divide_in_chunks(arr, el_count):
    start = 0
    end = el_count

    while end < len(arr):
        log.info("Make chunk: #{0} #{1}".format(start, end))
        yield arr[start:end]
        start = end
        end += el_count

    yield arr[start:]


def _translation_filter(pack):
    out = pack[0].rstrip(' ').rstrip('.')
    return len(out) > 0


def _unpack_translation(pack):
    src = pack[1].rstrip('.')
    out = pack[0].rstrip(' ').rstrip('.')
    return src, out


def _get_translations(words, source_lang, output_lang):
    translations = []

    for chunk in _divide_in_chunks(list(words), 100):
        translation_string = ". ".join(chunk)
        translated_result = translate.translator(source_lang, output_lang, translation_string)
        translations.extend(map(_unpack_translation,
                                filter(_translation_filter, translated_result[0])))

    return translations


def _aggregate_translations(output, translations):
    with open(output, 'w+', encoding='utf-8') as result_csv:
        csv_writer = csv.writer(result_csv, delimiter=',', lineterminator="\n")
        csv_writer.writerows(translations)


def translate2csv(args):
    log.basicConfig(level=log.INFO, format='%(message)s')

    words = _get_source_words(args.src_file)
    translations = _get_translations(words, args.src_lang, args.out_lang)
    _aggregate_translations(args.out_file, translations)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--src-file', type=str, help='Source text file location', required=True)
    parser.add_argument('-o', '--out-file', type=str, help='Output csv file location with translation', required=True)
    parser.add_argument('-l', '--src-lang', type=str, help='Source text language', required=True)
    parser.add_argument('-t', '--out-lang', type=str, help='Output translation language', required=True)
    parser.set_defaults(handler=translate2csv)

    args = parser.parse_args()
    args.handler(args)


if __name__ == "__main__":
    # run with params, for example:
    # >>> python translate2csv.py -s c:/input_book.txt -o translation_output.csv -l en -t ru
    main()
