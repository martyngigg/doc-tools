#!/usr/bin/env python
"""
    Creates a sitemap file for use the Google Custom Search tools
"""
from optparse import OptionParser
import os
import sys

#------------------------------------------------------------------------------

class Sitemap(object):

    def __init__(self, startdir, url_prefix):
        """
        Arguments:
          startdir (str): Root directory to start walk of site
          url_prefix (str): The prefix to give all locations within the sitemap
        """
        self.startdir = startdir
        self.url_prefix = url_prefix
        if not self.url_prefix.endswith("/"):
            self.url_prefix += "/"

    def build(self):
        """
        Constructs the sitemap of the html files
        """
        for dirname, dirnames, filenames in os.walk(self.startdir):
            for filename in filenames:
                if filename.endswith(".html"):
                    self.add_path(os.path.join(dirname, filename))

    def add_path(self, filepath):
        """
        Constructs a HTML link using the configured prefix
        and the relative path of the given filepath from the chosen
        current start directory and then adds it to the map

        Arguments:
          filepath (str): A filesystem path to a html file to add to the map
        """
        relpath = os.path.relpath(filepath, start=self.startdir)
        # URLs should always use unix-style path separators
        relpath = relpath.replace("\\", "/")
        # add to map
        self.add_location(self.url_prefix + relpath)

    def add_location(self, html_link):
        """
        Adds a URL to the sitemap

        Arguments:
          html_link (str): A full URL path to a resource that should appear in the map
        """
        raise NotImplementedError("New Sitemap types should inherit & override add_location()")

    def write(self, writer):
        """
        Outputs the map to the given object

        Arguments:
          writer (file-like object): An object with a write method that accepts a string
        """
        raise NotImplementedError("New Sitemap types should inherit & override write()")

#------------------------------------------------------------------------------

class TextSitemap(Sitemap):

    __index = None

    def __init__(self, startdir, url_prefix):
        super(TextSitemap, self).__init__(startdir, url_prefix)

        self.__index = []

    def add_location(self, html_link):
        self.__index.append(html_link)

    def write(self, writer):
        for line in self.__index:
            writer.write(line + "\n")

#------------------------------------------------------------------------------

def buildmap(startdir, url_prefix, format, outfilename):
    """
    Arguments:
      startdir (str): Root directory to start walk of site
      url_prefix (str): The prefix to give all locations within the sitemap
      format (str): String denoting format
      outfilename (str): Filename for the output. If None it is sent to sys.stdout
    """
    if format == "txt":
        sitemap = TextSitemap(startdir, url_prefix)
    else:
        raise ValueError("Unknown format '%s'. Currently supported formats={.txt}" % format)

    # Build
    sitemap.build()

    # Output
    if outfilename is None:
        writer = sys.stdout
    else:
        writer = open(outfilename, "w")

    sitemap.write(writer)
    writer.close()

#------------------------------------------------------------------------------

def main(argv):

    # Setup options
    parser = OptionParser(usage="%prog [options] STARTDIR")
    parser.add_option("-o", "--output", dest="output", metavar="FILENAME",
                      help="If provided, store the output in the given file."
                           "The format will be derived from the extension")
    parser.add_option("-p", "--prefix", dest="prefix", metavar="PREFIX",
                      default="http://docs.mantidproject.org/",
                      help="Replace the STARTDIR with this prefix on all locations")

    # Parse user arguments
    (options, args) = parser.parse_args(argv)

    if len(args) < 1 or len(args) > 1:
        print "ERROR: Incorrect number of arguments '%s'" % args
        print
        parser.print_help()
        sys.exit(1)

    if options.output is None:
        format = "txt"
        outfilename = None
    else:
        outfilename = options.output
        format = os.path.splitext(outfilename)[1].lstrip(".")

    prefix = options.prefix
    startdir = args[0]

    buildmap(startdir, prefix, format, outfilename)

#------------------------------------------------------------------------------

if __name__ == "__main__":
    main(sys.argv[1:]) # chop of the python part

