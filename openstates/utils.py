"""
Helper methods for parsing certain oddball formats in use by n>1 states.

These functions probably want to be moved into billy.scrape.utils, but at
the time of writing I didn't want to change the dependency to a non-release
build of billy.
"""
import os
import subprocess

def _is_executable(loc):
    """
    Check if a given file path or file name represents an executable file.

    Will check on the PATH if the filename does not include any / characters.
    """
    if os.sep in loc:
        return os.access(loc, os.X_OK)
    else:
        for d in os.environ['PATH'].split(':'):
            if _is_executable(os.sep.join((d, loc))):
                return True
    return False

def _get_executable(common_locations):
    """
    Given a list of common names for a particular program, return the first
    executable one.
    """
    executable_locations = [
        loc for loc in common_locations if _is_executable(loc)
    ]
    if not executable_locations:
        raise Exception('Could not find executable. Looked in: \n%s' % (
            "\n".join(common_locations)
        ))
    return executable_locations[0]

def _abiword_odt(in_file, format):
    """
    Use abiword to convert an ODT file to another format.

    See http://www.abisource.com/wiki/Command_line_options
    """
    exec_path = _get_executable([
        '/Applications/AbiWord.app/Contents/MacOS/AbiWord',
        '/Applications/MacPorts/AbiWord.app/Contents/MacOS/AbiWord',
        'abiword'
    ])
    cwd = '/tmp/'
    out_file = cwd + '.'.join((os.path.basename(in_file), format))
    subprocess.check_call('%s --to=%s %s' % (exec_path, out_file, in_file),
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

