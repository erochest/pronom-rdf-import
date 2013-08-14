#!/usr/bin/env python


"""\
This pages through the data on the Unified Digital Format Registry
(http://udfr.org/). It downloads each page and loads the search results into a
graph that it dumps out to the screen as Turtle.

**NB: The download feature on this has not been tested. However, the result
parsing has been run on downloads saved to the disk.**

"""


import codecs
import datetime
import math
import sys

from lxml import etree
import pystache
from rdflib import BNode, Graph, Literal, URIRef
import requests


ENDPOINT   = 'http://udfr.org/ontowiki/sparql/'
PAGE_SIZE  = 10000
QUERY_FILE = 'download.sparql.mustache'
NS         = 'http://www.w3.org/2005/sparql-results#'
XMLS       = 'http://www.w3.org/2001/XMLSchema#'
RDFS       = 'http://www.w3.org/2000/01/rdf-schema#'
SRESULTS   = 'http://www.w3.org/2005/sparql-results#'
ISO        = '%Y-%m-%dT%H:%M:%S'


def make_query(template, offset, page_size):
    return pystache.Renderer().render(
            template, {'offset': offset, 'page_size': page_size}
            )


def query(endpoint, sparql):
    response = requests.post(endpoint, data={'query': sparql})
    return etree.fromstring(response.text)


def get_results(ns, tree):
    xpath = '//{{{0}}}results/{{{0}}}result'.format(ns)
    return tree.iterfind(xpath)


def convert_datetime(iso_str):
    dt       = datetime.datetime.strptime(iso_str[:-6], ISO)
    (hr, mn) = iso_str[-6:].split(':')
    hr       = int(hr)
    offset   = datetime.timedelta(hours=hr, minutes=math.copysign(int(mn), hr))
    return Literal(dt - offset)


def convert_int(int_str):
    return Literal(int(int_str))


URI     = '{{{0}}}uri'.format(NS)
LITERAL = '{{{0}}}literal'.format(NS)


def identity(x):
    return Literal(x)


def xmls(datatype):
    return '{{{0}}}{1}'.format(XMLS, datatype)


def vxmls(datatype):
    return XMLS + datatype


def rdfs(datatype):
    return '{{{0}}}{1}'.format(RDFS, datatype)


def vrdfs(datatype):
    return RDFS + datatype


def sresults(datatype):
    return '{{{0}}}{1}'.format(SRESULTS, datatype)


VAL_CONVERTERS = {
    (URI, None)                              : URIRef,
    (LITERAL, vxmls('dateTime'))             : convert_datetime,
    (LITERAL, vxmls('string'))               : identity,
    (LITERAL, None)                          : identity,
    (LITERAL, vrdfs('Literal'))              : identity,
    (sresults('literal'), None)              : identity,
    (sresults('literal'), vxmls('dateTime')) : convert_datetime,
    (sresults('literal'), vxmls('integer'))  : convert_int,
    }


def get_val(child):
    key = (child.tag, child.get('datatype'))
    return VAL_CONVERTERS[key](child.text)


def get_triple(ns, result):
    triple = {}
    for binding in result.iterfind('{{{0}}}binding'.format(ns)):
        if len(binding) == 0:
            val = BNode()
        else:
            val = get_val(binding[0])
        triple[binding.get('name')] = val
    return (triple['s'], triple['p'], triple['o'])


def add_tree(graph, tree, ns):
    triples = ( get_triple(ns, r) for r in get_results(ns, tree) )
    for tr in triples:
        graph.add(tr)


def load_files(graph, files, ns):
    for fn in files:
        with open(fn) as f:
            tree = etree.parse(f)
        add_tree(graph, tree, ns)


def main():
    g = Graph()

    template = None
    with codecs.open(QUERY_FILE, encoding='UTF8') as f:
        template = pystache.parse(f.read())

    offset = 0
    while True:
        sparql  = make_query(template, offset, PAGE_SIZE)
        tree    = query(ENDPOINT, sparql)
        add_tree(g, tree, NS)
        offset += PAGE_SIZE

    sys.stdout.write(g.serialize(format='turtle'))


if __name__ == '__main__':
    main()

