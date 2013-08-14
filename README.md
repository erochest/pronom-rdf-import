
This imports some specific data from a dump of Pronom's linked data and outputs
it as JSON.

Currently, we're getting the Pronom dump from
[mpollice/LinkedOpenData](https://github.com/mpollice/LinkedOpenData).

This outputs a JSON object with extensions as properties and arrays of some
basic information about those extensions as output.

## Programs

`download.py` This pages through the data on the [Unified Digital Format
Registry](http://udfr.org/). It downloads each page and loads the search
results into a graph that it dumps out to the screen as Turtle.

> **NB: The download feature on this has not been tested. However, the result
> parsing has been run on downloads saved to the disk.**

`merge_graphs.py` This reads from one or more Turtle files to pre-populate
a graph and then walks a directory reading all the RDF/XML files in the
directory and merging their triples into the graph. It then dumps the final
graph out to STDOUT as Turtle.

This is to merge the output of the `download.py` script with the PRONOM data
found in the repository https://github.com/mpollice/LinkedOpenData.git.

`dump_risks.py` This takes a Turtle file containing the output of the PRONOM
and UDFR datasets and dumps out the file types, extensions, and risks to a JSON
file.

The query itself to generate the data is in a secondary SPARQL file, which is
specified on the command line and defaults to `query.sparql`.

## Output

The output of the `dump_risks.py` utility produces a tree of JSON objects.

The outermost object has two keys, `by_ext` and `by_mime`. These index the same
set of JSON objects by two of their keys.

Both of the indexes are maps/objects. The properties are file extensions in
one, and MIME types in the other.

The objects that they index have these keys:

* `mime` The file type's MIME type;
* `ext` The file type's extension;
* `risk` The file type's risk assessment;
* `format` The UDFR IRI for the file type; and
* `name` The `rdfs:label` for the file type.

So here's part of the output, just enough to show the structure and contents of
the file.

```json
{
    "by_ext": {
        "cdx": [
            {
                "mime": "chemical/x-cdx",
                "ext": "cdx",
                "risk": null,
                "format": "http://udfr.org/udfr/u1f355",
                "name": "Chemical Draw Exchange Format"
            }
        ],
        "jpe": [
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "High",
                "format": "http://udfr.org/udfr/u1f376",
                "name": "JPEG File Interchange Format, version 1.00"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Low",
                "format": "http://udfr.org/udfr/u1f376",
                "name": "JPEG File Interchange Format, version 1.00"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Medium",
                "format": "http://udfr.org/udfr/u1f376",
                "name": "JPEG File Interchange Format, version 1.00"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Medium",
                "format": "http://udfr.org/udfr/u1f376",
                "name": "JPEG File Interchange Format, version 1.00"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Low",
                "format": "http://udfr.org/udfr/u1f375",
                "name": "Raw JPEG Stream"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Low",
                "format": "http://udfr.org/udfr/u1f375",
                "name": "Raw JPEG Stream"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Medium",
                "format": "http://udfr.org/udfr/u1f375",
                "name": "Raw JPEG Stream"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "High",
                "format": "http://udfr.org/udfr/u1f377",
                "name": "JPEG File Interchange Format, version 1.01"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Low",
                "format": "http://udfr.org/udfr/u1f377",
                "name": "JPEG File Interchange Format, version 1.01"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Medium",
                "format": "http://udfr.org/udfr/u1f377",
                "name": "JPEG File Interchange Format, version 1.01"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Medium",
                "format": "http://udfr.org/udfr/u1f377",
                "name": "JPEG File Interchange Format, version 1.01"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Low",
                "format": "http://udfr.org/udfr/u1f378",
                "name": "JPEG File Interchange Format, version 1.02"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Medium",
                "format": "http://udfr.org/udfr/u1f378",
                "name": "JPEG File Interchange Format, version 1.02"
            },
            {
                "mime": "image/jpeg",
                "ext": "jpe",
                "risk": "Low",
                "format": "http://udfr.org/udfr/u1f378",
                "name": "JPEG File Interchange Format, version 1.02"
            }
        ],
        ...
    },
    "by_mime": {
        "application/x-tar": [
            {
                "mime": "application/x-tar",
                "ext": "tar",
                "risk": null,
                "format": "http://udfr.org/udfr/u1f623",
                "name": "Tape Archive Format"
            }
        ],
        ...
    }
}
```


