#!/usr/bin/env python
#############################################################
# ubi_reader
# (c) 2013 Jason Pruitt (jrspruitt@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#############################################################

import os
import sys

from ubi import ubi, get_peb_size
from ubi_io import ubi_file
from ui.common import output_dir


def extract_ubifs(ubi):
    for image in ubi.images:
        for volume in image.volumes:
            f = open('%s/img-%s_vol-%s.ubifs' % (output_dir, image.image_num, volume), 'wb')
            # Get UBIFS image from volume.
            for block in image.volumes[volume].reader(ubi):
                f.write(block)

if __name__ == '__main__':
    try:
        path = sys.argv[1]
        if not os.path.exists(path):
            print 'Path not found.'
            sys.exit(0)
    except:
        path = '-h'
    
    if path in ['-h', '--help']:
        print '''
Usage:
    $ ubifs_extract.py path/to/file/image.ubi

    Extracts the UBIFS from a UBI image and saves it
    to ubifs_<num>.img
    
    Works with binary data with multiple images inside.
        '''
        sys.exit(1)

    # Determine block size if not provided
    block_size = get_peb_size(path)
    # Create file object
    ufile = ubi_file(path, block_size)
    # Create UBI object
    uubi = ubi(ufile)
    # Run extract UBIFS
    extract_ubifs(uubi)
    sys.exit(1)