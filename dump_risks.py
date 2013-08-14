#!/usr/bin/env python

"""\
This takes a Turtle file containing the output of the PRONOM and UDFR datasets
and dumps out the file types, extensions, and risks to a JSON file.

The query itself to generate the data is in a secondary SPARQL file, which is
specified on the command line and defaults to `query.sparql`.

"""


import argparse
import collections
import json
import operator
import sys

import rdflib


QUERY_FILE = 'query.sparql'
INDEX_BY   = 'mime'


second = operator.itemgetter(1)


def tuple_to_dict(row):
    """\
    Convert a tuple into a dict.
    """
    (format, name, ext, mime, risk) = row
    obj = {
        'format' : format,
        'name'   : name,
        'ext'    : ext,
        'mime'   : mime,
        'risk'   : risk,
        }
    return obj


def index_query(rows, field=INDEX_BY):
    """This indexes the result rows by the first item, grouping by the second."""
    index = collections.defaultdict(list)
    for row in rows:
        ext = row[field]
        index[ext].append(row)
    return index


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Filter and dump data from Pronom.',
        )

    parser.add_argument(
        '-i', '--input', metavar='TURTLE', type=str, default=None,
        dest='input',
        help='The input Turtle file to read to generate the JSON from.'
        )
    parser.add_argument(
        '-q', '--query', metavar='SPARQL', type=str, default=QUERY_FILE,
        dest='query',
        help='The SPARQL file to select and project the data from the input. '
             '(default is "{0}".)'.format(QUERY_FILE)
        )

    opts = parser.parse_args(args)
    if opts.input is None:
        raise argparse.ArgumentTypeError('You must specify an input source.')

    return opts


def main(args=None):
    args = sys.argv[1:] if args is None else args
    opts = parse_args(args)

    graph = rdflib.Graph()
    graph.parse(opts.input, format='turtle')

    with open(opts.query) as f:
        rows = list(graph.query(f.read()))

    index = index_query( tuple_to_dict(row) for row in rows )

    sys.stdout.write(json.dumps(index))


if __name__ == '__main__':
    main()
