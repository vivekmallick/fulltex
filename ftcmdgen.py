#########################################################################
# Importing necessary files.
import subprocess
import sys
import os
import re

############################################################################
# Import local py files
from ftbasiccmd import *
from fterrhand import *

#############################################################################
# Functions involved in deciding which commands to run

def search_str_in_file (flname, str) :
    """To check if a string occurs in some line in a file."""
    try : 
        with open(flname) as f :
            found = False
            for l in f :
                if str in l :
                    found = True
    except :
        raise FullTexFileProcError(flname)
    return found

def need_bibtex (texfile) :
    """Checks whether we need to run bibtex"""
    auxfile = aux_file(texfile)
    str_in_aux_fl = '\\bibdata'
    str_in_tex_fl = '\\bibliography{'

    test1 = search_str_in_file(auxfile, str_in_aux_fl)
    test2 = search_str_in_file(texfile, str_in_tex_fl)
    
    return (test1 and test2)

def need_makeindex (texfile) :
    """Check whether we need to run makeindex"""
    idxfile = idx_file(texfile)
    packidx = '\\usepackage{makeidx}'

    test1 = search_str_in_file(texfile, packidx)
    test2 = os.path.isfile(idxfile)
    test3 = search_str_in_file(texfile, '\\makeindex')

    return (test1 and test2 and test3)

def need_rerun (texfile) :
    """Check whether we should rerun latex. This returns a boolean."""

    rerun_str = "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right."
    logfile = log_file(texfile)

    test1 = search_str_in_file(logfile, rerun_str)

    if test1 :
        rval = True
    else :
        rval = False

    return rval

#####################################################################
# Wrapper to run shell commands

def run_cmd(command_string) :
    """Given a command runs it in a shell."""
    try :
        subprocess.check_call(command_string.split())
    except Exception as e :
        print "Error in run_cmd : ", command_string, " : ", e
        raise FullTexRunCmdError (command_string)
    return None

