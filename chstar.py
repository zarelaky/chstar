#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# tar util for packing file with gb18030 charset filename encoded
import tarfile
import os
import sys
import string 
import argparse

class Mytar:
    
    def __init__(self):
        self.filter = None
        self.tar = None 
        self.charset='gb18030'
    def setcharset(self, charset):
        self.charset = charset 
        print(self.charset)

    # python tar.py target.tar.[ext] path 
    def pack(self, targetall, path):
        name,ext = os.path.splitext(targetall) 
        if ".xz" == ext:
            self.tar = tarfile.TarFile.open(name, "w")
        else:
            self.tar = tarfile.TarFile.open(targetall, "w:" + ext)
        for i in path:
            self.tar.add(i, filter=self.translateToGB18030)
        self.tar.close()

        if '.xz' == ext:
            print('waiting for xz utils')
            os.system('xz '+name)
            print('compress completed')



    def unpack(self, targetall, path):
        name,ext = os.path.splitext(targetall) 
        if ".xz" == ext:
            os.system('xz -d -k ' + targetall)
            self.tar = tarfile.TarFile.open(name, "r")
        else:
            self.tar = tarfile.TarFile.open(targetall, "r:" + targetall.split('.')[-1])
        
        self.tar.extractall(path=path, members=self.translateToUtf8(self.tar))
        self.tar.close() 
        if '.xz' == ext:
            os.system('rm -f ' + name)

    def translateToGB18030(self, tarinfo):
        name=None 
        try:
            name = tarinfo.name
            name = name.decode('utf-8').encode(self.charset)
            print(tarinfo.name)
        except Exception as ex:
            name = None
            print ex 
        if not None == name: 
            tarinfo.name = name;
        return tarinfo

    def translateToUtf8(self, members):
        for tarinfo in members:
            name=None 
            try:
                name = tarinfo.name
                name = name.decode(self.charset).encode("utf-8")
                print(name)
            except Exception as ex:
                name = None
                print ex 
            if not None == name: 
                tarinfo.name = name;
                yield tarinfo


if __name__ == "__main__":
    tar = Mytar()
    parser = argparse.ArgumentParser();
    parser.add_argument("-x", help="extract file, if no provided, archive will be created", action="store_const",const=1, default=0)
    parser.add_argument("--charset", help="charset for translating file name", default='gb18030')
    parser.add_argument("target", help="file want to save or extract" ,nargs=1)
    parser.add_argument("path", help="path which want to pack or extract", nargs='+')

    args = parser.parse_args(sys.argv[1:])
    tar.setcharset(args.charset)
    if args.x == 0:
        print 'packing ...'
        tar.pack(args.target[0], args.path)
    else:
        print 'unpacking ...'
        tar.unpack(args.target[0], args.path[0])




