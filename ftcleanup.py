###################################################################3
# Clean up functions for fulltex 
#######################################

#### Imports

import os
import re

#################################################

def extns (others=[], width=70) :
    ext_to_del = ['log', 'aux', 'idx', 'ind', 'lof', 'lot', 'out', 'toc',
            'acn', 'acr', 'alg', 'glg', 'glo', 'gls', 'ist', 'bbl', 'blg',
            'ilg']
    fullist = ext_to_del + others
    per_table = int((width - 15.0)/5.0)
    retlist = []
    pos = 0
    while pos < len(fullist) :
        no_in_line = 0
        line_lst = []
        pos_in_line = 0
        while pos_in_line < per_table and pos < len(fullist) :
            line_lst.append(fullist[pos])
            pos_in_line += 1
            pos += 1
        retlist.append(line_lst)

    return retlist

def files (texfile) :
    # Browses through the texfile and returns a list of all files which are
    # input/included
    fllist = [texfile[:-4]]
    with open(texfile) as f :
        for l in f :
            if 'include' in l :
                match = re.search("(\include{(?P<fl>.*)})", l)
                if match != None :
                    flname = match.group('fl')
                    if flname[-4:] == '.tex' :
                        flname = flname[:-4]
                    fllist.append(flname)
            if 'input' in l :
                match = re.search("(\input{(?P<fl>.*)})", l)
                if match != None :
                    flname = match.group('fl')
                    print flname
                    if flname[-4:] == '.tex' :
                        flname = flname[:-4]
                    fllist.append(flname)
    return fllist

def padton(s, n) :
    l = len(s)
    if l > n-1 :
        return "String too long"
    else :
        return s + ' ' * (n - l)


def delete_files (texfile, others=[], width=70) :
    for tab in extns(others, width) :
        print padton(' ', 15),
        for e in tab :
            print padton(e, 4),
        print
        for f in files(texfile) :
            print padton(f, 15),
            for e in tab :
                ftodel = f + '.' + e
                if os.path.isfile(ftodel) :
                    try :
                        os.remove(ftodel)
                        print padton(u' \u2714', 4),
                    except Exception :
                        print padton(' ?', 4),
                else :
                    print padton(' ', 4),
            print
        print "-" * width

def delete_files_w_opts(texfile, userOpt, others=[], width=70) :
    run_del = True
    run_del = run_del and (userOpt.user_opt('rm') == "Default")
    run_del = run_del and (not (userOpt.user_opt('synctex')))
    if run_del :
        delete_files(texfile, others, width)
