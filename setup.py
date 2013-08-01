
from distutils.core import setup


setup(
    name='pronom-rdf-import',
    version='0.0.1',
    description='Filter Pronom LOD into JSON.',
    author='Eric Rochester',
    author_email='erochest@virginia.edu',
    url='https://github.com/erochest/pronom-rdf-import',

    scripts=['pronom_dump'],

    requires=[
        'rdflib',
        ],
    )

