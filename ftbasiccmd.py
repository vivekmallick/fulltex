##########################################################################
# Importing library
from ftflnames import *

##########################################################################
# Commands depending upon output type

def latex_cmd(compilation_type='pdf') :
    """Decides which flavour of tex/latex to use"""
    compiler_dict = {
            'dvi' : 'latex',
            'pdf' : 'pdflatex',
            'dvipdf' : 'latex',
            'ps' : 'latex',
            'tex' : 'tex',
            'texps' : 'tex',
            'texpdf' : 'tex'
            }

    if compilation_type in compiler_dict.keys() :
        cmd = compiler_dict[compilation_type]
    else :
        raise FullTexTypeError(compilation_type)
        cmd = None
    return cmd

def post_compile_seq (texfile, outputtype) :
    pcs_dict = {
        'dvi' : [],
        'ps' : ['dvips ' + dvi_file(texfile)],
        'dvipdf' : ['dvipdf ' + dvi_file(texfile)],
        'pdf' : [],
        'tex' : [],
        'texps' : ['dvips ' + dvi_file(texfile)],
        'texpdf' : ['dvipdf ' + dvi_file(texfile)]
        }

    if outputtype in pcs_dict.keys() :
        rval = pcs_dict[outputtype]
    else :
        raise FullTexTypeError(outputtype)
    return rval


###############################################################################33
# Functions generating shell commands

def generate_tex_cmd(compilation_type,
        filename,
        latex_options=[]
        ) :
    """Creates the latex command line to be run"""
    
    cmd = latex_cmd(compilation_type)

    tex_cmd = cmd + " -interaction=nonstopmode "
    for opt in latex_options :
        tex_cmd = tex_cmd + opt + " "

    tex_cmd = tex_cmd + filename
    return tex_cmd

def bibtex_cmd (texfile) :
    """Generates the bibtex command"""
    cmd = 'bibtex '
    flname = texfile[:-4]
    cmd = cmd + flname
    return cmd


def makeindex_cmd (texfile) :
    """Generates the makeindex command"""
    cmd = 'makeindex '
    flname = texfile[:-4]
    cmd = cmd + flname
    return cmd



