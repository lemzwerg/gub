import os
import re

import download
import gub
import cross

class Gcc (cross.Gcc):
    def patch (self):
        for f in ['%(srcdir)s/gcc/config/i386/mingw32.h',
             '%(srcdir)s/gcc/config/i386/t-mingw32']:
            self.file_sub ([('/mingw/include','/usr/include'),
                    ('/mingw/lib','/usr/lib'),
                    ], f)

# UGH: MI
class Mingw_runtime (gub.Binary_package, gub.Sdk_package):
    def untar (self):
        gub.Binary_package.untar (self)
        self.system ('mkdir -p %(srcdir)s/root/usr')
        self.system ('cd %(srcdir)s/root && mv * usr',
              ignore_error=True)

class Cygcheck (gub.Binary_package):
    "Only need the cygcheck.exe binary."
    def __init__ (self, settings):
        gub.Binary_package.__init__ (self, settings)
        self.with (version='1.5.18-1', mirror=download.cygwin_bin, format='bz2',
                   builddeps=['mingw-runtime'])
        
    def untar (self):
        gub.Binary_package.untar (self)

        file = self.expand ('%(srcdir)s/root/usr/bin/cygcheck.exe')
        cygcheck = open (file).read ()
        self.system ('rm -rf %(srcdir)s/root')
        self.system ('mkdir -p %(srcdir)s/root/usr/bin/')
        open (file, 'w').write (cygcheck)

    def basename (self):
        f = gub.Binary_package.basename (self)
        f = re.sub ('-1$', '', f)
        return f


# UGH: MI
class W32api (gub.Binary_package, gub.Sdk_package):
    def untar (self):
        gub.Binary_package.untar (self)
        self.system ('mkdir -p %(srcdir)s/root/usr')
        self.system ('cd %(srcdir)s/root && mv * usr',
              ignore_error=True)

def get_cross_packages (settings):
    return [cross.Binutils (settings).with (version='2.16.1', format='bz2'),
            Gcc (settings).with (version='4.1.0',
                                 mirror=download.gcc_41,
                                 builddeps=['binutils', 'mingw-runtime', 'w32api']),
            Mingw_runtime (settings).with (version='3.9', mirror=download.mingw),
            W32api (settings).with (version='3.5', mirror=download.mingw),
            ]


def change_target_packages (packages):
    cross.change_target_packages (packages)

    for p in packages:
        gub.change_target_dict (p,
                    {
            'DLLTOOL': '%(tool_prefix)sdlltool',
            'DLLWRAP': '%(tool_prefix)sdllwrap',
            })
