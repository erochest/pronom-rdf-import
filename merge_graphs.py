#!/usr/bin/env python


import argparse
import os
import sys

import rdflib
import rdflib.term


def read_input_dirs(graph, dirnames):
    """Return a Graph created from the RDF files in all directory trees. """
    for dirname in dirnames:
        for (root, dirs, files) in os.walk(dirname):
            for fn in files:
                ext = os.path.splitext(fn)[1]
                if ext != '.rdf':
                    continue
                fn = os.path.join(root, fn)
                sys.stderr.write('parsing {0}...\n'.format(fn))
                graph.parse(fn)
    return graph


def clean_term(term):
    if isinstance(term, rdflib.URIRef):
        term = rdflib.URIRef(term.strip().replace(' ', '+'))
    return term


def clean_triple(triple):
    (s, p, o) = triple
    return (clean_term(s), clean_term(p), clean_term(o))


def clean_graph(graph):
    is_valid_uri = rdflib.term._is_valid_uri
    to_clean = set()

    for tr in graph:
        uris = ( t for t in tr if isinstance(t, rdflib.URIRef) )
        if not all( is_valid_uri(uri) for uri in uris ):
            to_clean.add(tr)

    for tr in to_clean:
        graph.remove(tr)
        graph.add(clean_triple(tr))


def parse_args(args):
    parser = argparse.ArgumentParser(
        description='Filter and dump data from Pronom.',
        )

    parser.add_argument(
        '-t', '--turtle', metavar='TURTLE', type=str, action='append',
        dest='turtle',
        help='The TURTLE files to preload the graph with '
             '(can be more than one).',
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

    graph = rdflib.Graph()
    if opts.turtle is not None:
        for ttl in opts.turtle:
            if os.path.exists(ttl):
                sys.stderr.write('Parsing {0}...\n'.format(ttl))
                graph.parse(ttl, format='turtle')
    read_input_dirs(graph, opts.input_dirs)

    sys.stderr.write('Cleaning up...\n')
    clean_graph(graph)

    sys.stderr.write('Dumping to STDOUT...\n')
    sys.stdout.write(graph.serialize(format='turtle'))


if __name__ == '__main__':
    main()
