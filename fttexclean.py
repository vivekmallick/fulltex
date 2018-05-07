#!/usr/bin/python


#########################################################################
# Personal Packages

from fterrhand import *
from ftcmdgen import *
from ftcleanup import *
from fthelp import *

###########################################################################
# Class to store the user options

class UserOptions :
    def __init__(self, optLst) :
        # optLst = option list. Process option list to get bibopt, 
        #          mkidxopt, rmopt and fltype
        lo = len(optLst)

        # Defaults
        bibopt = "Auto"
        mkidxopt = "Auto"
        rmopt = "Default"
        fltype = "pdf"
        latexswitches = []
        texfilename = []
        syncTex = False
        needsHelp = False # Var is called needsHelp
                          # method -      needHelp

        # Main option processing loop
        optionProcessed = 0
        continueLoop = True
        while continueLoop :
            currOpt = optLst[optionProcessed]
            if currOpt == "-bibtex" :
                bibopt = "False"
            elif currOpt == "+bibtex" :
                bibopt = "True"
            elif currOpt == "?bibtex" :
                bibopt = "Auto"
            elif currOpt == "-makeindex" :
                mkidxopt = "False"
            elif currOpt == "+makeindex" :
                mkidxopt = "True"
            elif currOpt == "?makeindex" :
                mkidxopt = "Auto"
            elif currOpt == "+synctex" :
                syncTex = True
            elif currOpt == "-synctex" :
                syncTex = False
            elif currOpt == "--rm" :
                optionProcessed += 1
                if optionProcessed >= lo :
                    print "UserOptions : Error : --rm does not have an option."
                else :
                    rmopt = optLst[optionProcessed]
            elif currOpt == "--output" :
                optionProcessed += 1
                if optionProcessed >= lo :
                    print "UserOptions : Error : --output does not have an option."
                else :
                    fltype = optLst[optionProcessed]
            elif currOpt == "--latex" :
                optionProcessed += 1
                if optionProcessed >= lo :
                    print "UserOptions : Error : --latex does not have an option."
                else :
                    latexswitches.append(optLst[optionProcessed])
            elif currOpt == "--file" :
                optionProcessed += 1
                if optionProcessed >= lo :
                    print "UserOptions : Error : --file does not have an option."
                else :
                    texfilename.append(optLst[optionProcessed])
            elif currOpt == "--help" :
                needsHelp = True
            else :
                if optionProcessed == lo - 1 :
                    texfilename.append(optLst[optionProcessed])
                else :
                    print "UserOptions : Error : Unknown command " + optLst[optionProcessed]

            # End of the if blocks

            optionProcessed += 1

            if optionProcessed >= lo :
                continueLoop = False

        # End of the while loop : Main option processing loop
        

        self.bibopt = bibopt
        self.mkidxopt = mkidxopt
        self.rmopt = rmopt
        self.fltype = fltype
        self.latexswitches = latexswitches
        self.texfilename = texfilename
        self.syncTex = syncTex
        self.needsHelp = needsHelp

    def user_opt(self, opttype) :
        if opttype == 'bibtex' :
            retval = self.bibopt
        elif opttype == 'makeindex' :
            retval = self.mkidxopt
        elif opttype == 'rm' :
            retval = self.rmopt
        elif opttype == 'output' :
            retval = self.fltype
        elif opttype == 'texfilename' :
            retval = self.texfilename
        elif opttype == 'latexswitches' :
            retval = self.latexswitches
        elif opttype == 'synctex' :
            retval = self.syncTex
        else :
            print "Error! Unknown option type."
            retval = "Unknown type"
        return retval

    def needHelp(self) :
        return self.needsHelp

    # def enable_synctex(self) :
        # self.latexswitches.append('-synctex=1')


#########################################################################
# Actual compilation

def separate( width = 70) :
    print " "
    print "*" * width
    print " " 

def compile_tex (texfile, userOpt, width=70 , maxTries=6) :
    """Compiles latex given the tex file name, output type and the commands
    to be sent to the latex command."""
    
    # Set local variables depending on userOpt
    ltxCmdOpts = userOpt.user_opt('latexswitches')
    bibOpt = userOpt.user_opt('bibtex')
    indexOpt = userOpt.user_opt('makeindex')
    outputtype = userOpt.user_opt('output')


    runAgain = False
    if userOpt.user_opt('synctex') :
        newLtxCmdOpts = ltxCmdOpts + ['-synctex=1']
    else :
        newLtxCmdOpts = ltxCmdOpts
    run_cmd(generate_tex_cmd(outputtype, texfile, newLtxCmdOpts))

    separate(width)

    runAgain = need_rerun(texfile)

    if (bibOpt == 'Auto' and need_bibtex(texfile)) or bibOpt == 'True' :
        run_cmd(bibtex_cmd(texfile))
        separate(width)
        runAgain = True
        
    if (indexOpt == 'Auto' and need_makeindex(texfile)) or indexOpt == 'True' :
        run_cmd(makeindex_cmd(texfile))
        separate(width)
        runAgain = True

    n = maxTries
    while (runAgain and n > 0) :
        run_cmd(generate_tex_cmd(outputtype, texfile, newLtxCmdOpts))
        n = n - 1
        separate(width)
        runAgain = need_rerun(texfile)

    if n == 0 :
        print "MAXIMUM NUMBER OF TRIES EXCEEDED."

    # Run winding up commands
    for cmd in post_compile_seq(texfile, outputtype) :
        print "Running : ",cmd
        run_cmd(cmd)
        separate(width)

# Code for compile; delete suite; 
### WARNING !!!!! 
# This function needs to be upgraded to
# include synctex and the above should be moved to a new file. It makes no
# sense to automatically call delete_files at every run.

def tex_and_clean(userTags, helpfilename='/home/vmallick/.fulltex/help.txt') :
    if userTags.needHelp() :
        print "Needs help."
        print_help(helpfilename)
    else :
        print "All fine."
        if len(userTags.user_opt('texfilename')) == 0 :
            print "What happened to the filename?"
        else :
            for texfile in userTags.user_opt('texfilename') :
                print "Process " + texfile
                compile_tex(texfile, userTags)
                delete_files(texfile)

# Main code
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
    tex_and_clean(userTags, helpfilename="./help.txt")
