import download
import gub
import os
import re

class Mingw_runtime (gub.Binary_package):
	def set_download (self, mirror=download.gnu, format='gz', download=gub.Target_package.wget):
		gub.Package.set_download (self, mirror, format, download)
		self.url = re.sub ('mingw-runtime/', 'mingw/', self.url)
		self.url = re.sub ('w32api/', 'mingw/', self.url)
		
class Cygwin (gub.Binary_package):
	"Only need the cygcheck.exe binary."
	
	def untar (self):
		gub.Binary_package.untar (self)

		file = '%s/root/usr/bin/cygcheck.exe' % self.srcdir ()
		cygcheck = open (file).read ()
		self.system ('rm -rf %(srcdir)s/root')
		self.system ('mkdir -p %(srcdir)s/root/usr/bin/')
		open (file, 'w').write (cygcheck)

	def basename (self):
		f = gub.Binary_package.basename (self)
		f = re.sub ('-1$', '', f) 
		return f

class W32api (Mingw_runtime):
	pass

class Regex (gub.Target_package):
	pass

class Gs (gub.Binary_package):
	def untar (self):
		gub.Binary_package.untar (self)
		self.system ('cd %(srcdir)s && mv root/gs-%(version)s/* .')

	def patch (self):
		gs_prefix = '/usr/share/gs'
		self.dump ('''
cat > Makefile <<EOF
default:
	@echo done
all: default
install:
	mkdir -p %(install_prefix)s
	tar -C %(srcdir)s -cf- bin | tar -C %(install_prefix)s -xvf-
	mkdir -p %(install_root)s/%(gs_prefix)s
	tar -C %(srcdir)s -cf- fonts lib Resource | tar -C %(install_root)s/%(gs_prefix)s -xvf-
	fc-cache %(install_root)s/%(gs_prefix)s/fonts
	mkdir -p %(install_prefix)s/share/doc/gs/html
	tar -C %(srcdir)s/doc -cf- --exclude='[A-Z]*[A-Z]' . | tar -C %(install_prefix)s/share/doc/gs/html -xvf-
	tar -C %(srcdir)s/doc -cf- --exclude='*.htm*' . | tar -C %(install_prefix)s/share/doc/gs/html -xvf-
EOF
''',
			   '%(srcdir)s/configure',
			   env=locals ())
		os.chmod ('%(srcdir)s/configure' % self.package_dict (), 0755)


class LilyPad (gub.Target_package):
	def makeflags (self):
		# FIXME: better fix Makefile
		return gub.join_lines ('''
ALL_OBJS='$(OBJS)'
WRC=/usr/bin/wrc
CPPFLAGS=-I%(system_root)s/usr/include
RC='$(WRC) $(CPPFLAGS)'
LIBWINE=
LIBPORT=
MKINSTALLDIRS=%(srcdir)s/mkinstalldirs
INSTALL_PROGRAM=%(srcdir)s/install-sh
''')
		
	def compile_command (self):
		return gub.Target_package.compile_command (self) \
		       + self.makeflags ()

	def install_command (self):
		return gub.Target_package.broken_install_command (self) \
		       + self.makeflags ()

def get_packages (settings):
	return (
		Mingw_runtime (settings).with (version='3.9', mirror=download.sf),
		W32api (settings).with (version='3.5', mirror=download.sf),
		Cygwin (settings).with (version='1.5.18', mirror=download.cygwin, format='bz2'), 
		Regex (settings).with (version='2.3.90-1', mirror=download.lp, format='bz2'),
		Gs (settings).with (version='8.15-1', mirror=download.lp, format='bz2'),
		LilyPad (settings).with (version='0.0.7-1', mirror=download.lp, format='bz2'),
		)

