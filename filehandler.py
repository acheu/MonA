#Support program for handling files in directory
import os


def GetFileList(videorep):
    a = os.listdir(videorep)
    return a

def RMFileFromList(rep, vidl):
    if isinstance(vidl, list):
        for itt in vidl:
            os.remove(rep + itt)
    else:
        os.remove(rep + vidl)

