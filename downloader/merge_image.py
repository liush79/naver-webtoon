#!/usr/bin/python

import getopt
import sys
import Image
import os


def merge_image(output, path_list, png=False):
    width = 0
    height = 0
    ext = '.jpg'
    type = 'JPEG'

    if png:
        ext = '.png'
        type = 'PNG'

    try:
        # print path_list
        # get total image size
        for path in path_list:
            img = Image.open(path)
            if width < img.size[0]:
                width = img.size[0]
            height += img.size[1]

        if height > 65530:
            ext = '.png'
            type = 'PNG'

        new_img = Image.new("RGB", (width, height), "white")
        height = 0

        for path in path_list:
            img = Image.open(path)
            new_img.paste(img, (0, height))
            height += img.size[1]

        new_img.save(output+ext, type, subsampling=0, quality=95)

        return True
    except Exception, e:
        print "ERROR: " + str(e)
        return False


def usage():
    print '====================================================='
    print 'usage: merge_image.exe <folder name>'
    print '\t example: merge_image.exe -d myfolder'
    print '\t example: merge_image.exe -p -d myfolder (png)'
    print '====================================================='
    sys.exit(1)


if __name__ == '__main__':
    folder_name = None
    type_png = False
    opts = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hpd:", ["help", "png", "directory="])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for opt, arg in opts:
        if (opt == "-p") or (opt == "--png"):
            type_png = True
        elif (opt == "-d") or (opt == "--directory"):
            folder_name = arg
        elif (opt == "-h") or (opt == "--help"):
            usage()

    if folder_name is None:
        usage()

    for root, dirs, files in os.walk(folder_name):
        idx = root.rfind('\\')
        print 'directory:', root
        print 'files:', files
        if idx == -1:   # root directory
            output_name = '%s\\%s_merge' % (root, root)
        else:
            folder = root[idx + 1:]
            output_name = '%s\\%s_merge' % (root, folder)
        flist = []
        for _file in files:
            flist.append('%s\\%s' % (root, _file))
        merge_image(output_name, flist, type_png)
    print 'Finish !!'

