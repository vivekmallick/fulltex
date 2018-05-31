#!/usr/bin/python

import time

#########################################################################
# Personal Packages

from fttexclean import *

# from fterrhand import *
# from ftcmdgen import *
# from ftcleanup import *
# from fthelp import *

#########################################################################
# Code to be used in run_with_synctex

def write_gvim_cmd_file(gvim_cmd_file, texfilename) :
    with open(gvim_cmd_file, 'w') as gvimfile :
        gvimfile.write("nnoremap wt ::w<Enter>:!touch triggertex<Enter><Enter>")
        basezath = "nnoremap wv ::exec \"!zathura --synctex-forward=\" . line(\".\") . \":\" . col(\".\") . \":\" . expand(\"%\") . \" " + pdf_file(texfilename) + "\"<Enter><Enter>"
        gvimfile.write("\n")
        gvimfile.write(basezath)
        currdir = os.getcwd()
        gvimfile.write("\n")
        gvimfile.write("cd " + currdir)
        gvimfile.write("\n")

def launch_gvim(gvim_cmd_file, gvimservername, texfilename) :
    write_gvim_cmd_file(gvim_cmd_file, texfilename)
    gvim_cmd = "gvim --servername " + gvimservername + " -S " + gvim_cmd_file
    print "Launch: " + gvim_cmd
    gvim_openfile_cmd = "gvim --servername " + gvimservername + " --remote " + texfilename
    print "Run: " + gvim_openfile_cmd
    gvim_set_dir_init = "gvim --servername " + gvimservername + " --remote-send"
    gvim_set_dir_tail = ":cd " + os.getcwd() + "<Enter><Enter>"
    print "Run: " + gvim_set_dir_init + "\"" + gvim_set_dir_tail + "\""
    gvim_set_dir_list = gvim_set_dir_init.split() + [gvim_set_dir_tail]

    try:
        run_cmd(gvim_cmd)
        time.sleep(2)
        run_cmd(gvim_openfile_cmd)
        time.sleep(10)
        # run_cmd(gvim_set_dir) This does not work
        subprocess.check_call(gvim_set_dir_list)
    except Exception as e:
        print "launch_gvim: encountered exception " + e


def launch_zathura(texfile, gvimservername) :
    zathura_cmd_init = "zathura --fork -x "
    zathura_gvim_cmd = "gvim --servername " + gvimservername + " --remote +%{line} %{input}"
    zathura_end = pdf_file(texfile)
    zathura_list = zathura_cmd_init.split() + [zathura_gvim_cmd, zathura_end]
    try :
        subprocess.check_call(zathura_list)
    except Exception as e :
        print"launch_zathura: failed"


def is_server_running(gvimservername) :
    gvimlist = subprocess.check_output(['gvim', '--serverlist'])
    if gvimlist.find(gvimservername) > -1:
        retval = True
    else :
        retval = False
    return retval



###########################################################################
# Main code
# Decide if one needs to run a synctex loop. Then set up the loop

def need_synctex(userOpts) :
    return userOpts.user_opt('synctex')

def run_with_synctex(userTags, texfile) :
    print "run_with_synctex: May have bugs"
    gvim_cmd_file="fulltexgvim.vim"
    gvimservername=texfile[:-4].upper()

    # Launch gvim and zathura
    launch_gvim(gvim_cmd_file, gvimservername, texfile)
    launch_zathura(texfile, gvimservername)

    # Now run the loop
    while is_server_running(gvimservername):
        if os.path.isfile('triggertex'):
            try :
                # Run with synctex
                # userTags.enable_synctex()
                tex_and_clean(userTags, helpfilename="./help.txt")
            except Exception:
                print "Compilation failed"
                subprocess.call(['xmessage', 'Compilation failed'])
            os.remove('triggertex')
        time.sleep(5)
    os.remove(gvim_cmd_file)
    # os.remove(synctex_file(texfile))


# The following is for testing.

if __name__ == "__main__" :
    no_args = len(sys.argv)
    if no_args == 1 :
        print "We at least need a filename."
        exit(1)

    userTags = UserOptions(sys.argv[1:])
    print "bibtex : " + userTags.user_opt('bibtex')
    print "makeindex : " + userTags.user_opt('makeindex')
    print "rm : " + userTags.user_opt('rm')
    print "output type : " + userTags.user_opt('output')
    print "tex filename : " + userTags.user_opt('texfilename').__str__()
    print "latexswitches : " + userTags.user_opt('latexswitches').__str__()
    print "synctex : " + userTags.user_opt('synctex').__str__()

    if need_synctex(userTags) :
        texfile=userTags.user_opt('texfilename')[0]
        run_with_synctex(userTags, texfile)
    else :
        tex_and_clean(userTags, helpfilename="./help.txt")
