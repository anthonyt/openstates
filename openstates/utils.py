"""
Helper methods for parsing certain oddball formats in use by n>1 states.

These functions probably want to be moved into billy.scrape.utils, but at
the time of writing I didn't want to change the dependency to a non-release
build of billy.
"""
import os
import subprocess

def _abiword_odt(in_file, format):
    """
    Use abiword to convert an ODT file to another format.

    See http://www.abisource.com/wiki/Command_line_options
    """
    cwd = '/tmp/'
    out_file = cwd + '.'.join((os.path.basename(in_file), format))
    subprocess.check_call('abiword --to=%s %s' % (out_file, in_file),
                          shell=True, cwd=cwd)
    return out_file

def odt_to_txt(odt_file):
    """
    Given the full path to an .odt file, create a new .txt file and return
    its full path.

    TODO: Find a way to do this without relying on abiword.
          e.g. http://www.artofsolving.com/opensource/jodconverter
            or http://stosberg.net/odt2txt/
    """
    return _abiword_odt(odt_file, 'txt')

def odt_to_html(odt_file):
    """
    Given the full path to an .odt file, create a new .html file and return
    its full path.

    TODO: Find a way to do this without relying on abiword.
          e.g. http://www.artofsolving.com/opensource/jodconverter
    """
    return _abiword_odt(odt_file, 'html')

