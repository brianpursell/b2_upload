import os
import sys

def replace_hashes(dir):
    pieces = dir.split(' ')  
    underscored = ('_').join(pieces)

    if dir != underscored:
        print 'renaming'
        os.rename(dir, underscored)

    if os.path.isdir(underscored):
        for filename in os.listdir(underscored): 
            path = os.path.join(underscored, filename)
            replace_hashes(path)

replace_hashes(sys.argv[1])