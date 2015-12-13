def print_help (helpfilename) :
    try :
        with open(helpfilename, 'r') as helpfile :
            for line in helpfile :
                print line,
            print 
    except Exception:
        print "Help file not found."


if __name__ == "__main__" :
    print_help('help.txt')
