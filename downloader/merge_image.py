#!/usr/bin/python

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

        new_img.save(output+ext, type)

        return True
    except Exception, e:
        print "ERROR: " + str(e)
        return False

if __name__ == '__main__':
    list = []
    if len(sys.argv) == 1:
        print 'usage: merge_image.exe <folder name>'
        print '\t example: merge_image.exe myfolder'
    if len(sys.argv) == 2:  # select folder
        folder_name = sys.argv[1]
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
            merge_image(output_name, flist)
        print 'Finish !!'
    else:
        for argv in sys.argv[1:]:
            list.append(argv)
        merge_image(list[0], list[1:])

