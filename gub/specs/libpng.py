from gub import targetbuild
from gub import toolsbuild 

class Libpng (targetbuild.AutoBuild):
    source = 'http://surfnet.dl.sourceforge.net/sourceforge/libpng/libpng-1.2.8-config.tar.gz'

    def get_dependency_dict (self):
        return {'':['zlib']}
    
    def get_build_dependencies (self):
        return ['zlib-devel', 'tools::autoconf', 'tools::automake', 'tools::libtool']

    def name (self):
        return 'libpng'

    def patch (self):
        self.file_sub ([('(@INSTALL.*)@PKGCONFIGDIR@',
                r'\1${DESTDIR}@PKGCONFIGDIR@')],
               '%(srcdir)s/Makefile.in')
        self.file_sub ([('(@INSTALL.*)@PKGCONFIGDIR@',
                r'\1${DESTDIR}@PKGCONFIGDIR@')],
               '%(srcdir)s/Makefile.am')

    def configure (self):
        targetbuild.AutoBuild.configure (self)
        # # FIXME: libtool too old for cross compile
        self.update_libtool ()

    def compile_command (self):
        c = targetbuild.AutoBuild.compile_command (self)
        ## need to call twice, first one triggers spurious Automake stuff.                
        return '(%s) || (%s)' % (c,c)
    
class Libpng__tools (toolsbuild.AutoBuild, Libpng):
    source = Libpng.source
    def get_build_dependencies (self):
        return ['libtool']
    def patch (self):
        Libpng.patch (self)
