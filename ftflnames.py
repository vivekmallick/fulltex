#############################################################################
# Deducing secondary file names

def aux_file (texfile) :
    """Computes the aux file name from the tex file name."""
    return (texfile[:-3] + 'aux')

def idx_file (texfile) :
    """Computes the (makeindex) idx file name from the tex file name."""
    return (texfile[:-3] + 'idx')

def dvi_file (texfile) :
    """Computes the dvi file name from the tex file name."""
    return (texfile[:-3] + 'dvi')

def log_file (texfile) :
    """Computes the log file name from the tex file name."""
    return (texfile[:-3] + 'log')

def pdf_file(texfile) :
    """Name of the pdf file"""
    return (texfile[:-3] + 'pdf')

def synctex_file(texfile) :
    """Name of the synctex file"""
    return (texfile[:-3] + 'synctex.gz')
