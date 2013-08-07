#!/usr/bin/env python

# TODO: This should just take the output Turtle and transform it into the
# output JSON.


import argparse
import collections
import itertools
import json
import operator
import os
import re
import sys

from merge_graphs import read_input_dirs


QUERY_FILE    = 'query.sparql'
RE_FINAL_NAME = re.compile(r'\w+$')


second = operator.itemgetter(1)


def tuples_to_dict(id_uri, rows, name_re=RE_FINAL_NAME):
    """\
    Convert a set of tuple that share a subject IRI into a sequence of dicts.
    """
    accum = {}

    for (_, _, p, o) in rows:
        match = name_re.search(p)
        name = match.group(0) if match is not None else p
        accum[name] = o

    return accum


def index_query(exts):
    """This indexes the result rows by the first item, grouping by the second."""
    index = collections.defaultdict(list)

    exts.sort(key=second)
    for (iri, rows) in itertools.groupby(exts, second):
        rows = list(rows)
        ext  = rows[0][0]
        rowd = tuples_to_dict(iri, rows)
        rowd.setdefault('IRI', iri)
        rowd.setdefault('Extension', ext)
        index[ext].append(rowd)

    return index


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Filter and dump data from Pronom.',
        )

    parser.add_argument(
        'input_dirs', metavar='INPUT_DIRS', type=str, default='.', nargs='*',
        help='The directory of input RDF/XML files to walk (default={0}).'.format(
            os.getcwd(),
            )
        )

    return parser.parse_args(args)


def main(args=None):
    args = sys.argv[1:] if args is None else args
    opts = parse_args(args)

    graph = read_input_dirs(opts.input_dirs)
    with open(QUERY_FILE) as f:
        exts = list(graph.query(f.read()))
    index = index_query(exts)
    sys.stdout.write(json.dumps(index))


if __name__ == '__main__':
    main()
