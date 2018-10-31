import os 
import sys

def mark_done(path, filename):
    src = os.path.join(path, filename)
    done = 'done.' + filename
    dest = os.path.join(path, done)
    os.rename(src, dest)

    print 'renamed: ' + dest