# This file contains classes to handle exceptions in the fulltex program.

#########################################################################
# Exception Classes :

class FullTexError (Exception) :
    """Base exception class for FullTex"""
    pass

class FullTexTypeError (FullTexError) :
    """Exception class for unidentified output type"""
    def __init__(self, given_type) :
        self.type = given_type
    def __str__(self) :
        return ("Unidentified type : " + self.type)

class FullTexRunCmdError (FullTexError) :
    """Exception call failing shell codes"""
    def __init__(self, cmd_string) :
        self.cmd = cmd_string
    def __str__(self) :
        return ("Non zero exit on command : " + self.cmd)

class FullTexFileProcError (FullTexError) :
    """Exception Class for file processing errors"""
    def __init__(self, flname) :
        self.filename = flname
    def __str__(self) :
        return ("Error processing file : " + self.filename)



if __name__ == '__main__' :
    try :
        raise FullTexError('The ERROR')
    except FullTexError as e :
        print e
    try :
        raise FullTexTypeError('pdf')
    except FullTexError as e :
        print e
    try :
        raise FullTexRunCmdError('let there be light')
    except FullTexError as e :
        print e
    try :
        raise FullTexFileProcError('gamma')
    except FullTexError as e :
        print e

    print """
    
The output should be
______________________________________________________
The ERROR
Unidentified type : pdf
Non zero exit on command : let there be light
Error processing file : gamma
_____________________________________________________
"""
