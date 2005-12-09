import glob
import re
import gub
import download

from gub import join_lines

class Darwin_sdk (gub.Binary_package):
	def file_name (self):
		return 'darwin-sdk.tar.gz'

	def patch (self):
		pat = self.settings.system_root + '/usr/lib/*.la'
		for a in glob.glob (pat):
			self.file_sub ([(r' (/usr/lib/.*\.la)', '%(system_root)s\1')], a)

	def install (self):

		# don't add usr/ to root.
		self.system ('mkdir -p %(install_root)s/')
		self.system ('tar -C %(srcdir)s/root -cf- . | tar -C %(install_root)s/ -xvf-')

		
		
	
class Odcctools (gub.Cross_package):
	def install_prefix (self):
		return self.settings.tooldir
	def configure (self):
		gub.Cross_package.configure (self)

		## remove LD64 support.
		self.file_sub ([('ld64','')],
			       self.builddir () + '/Makefile')
class Gcc (gub.Cross_package):
	def patch (self):
		self.file_sub ([('/usr/bin/libtool', '%(tooldir)s/bin/powerpc-apple-darwin7-libtool')],
			       '%(srcdir)s/gcc/config/darwin.h')

	def configure_command (self):
		cmd = gub.Cross_package.configure_command (self)
		cmd += '''
--prefix=%(tooldir)s 
--program-prefix=%(target_architecture)s-
--with-as=%(tooldir)s/bin/powerpc-apple-darwin7-as  
--with-ld=%(tooldir)s/bin/powerpc-apple-darwin7-ld  
--enable-static
--enable-shared  
--enable-libstdcxx-debug 
--enable-languages=c,c++ ''' % self.settings.__dict__
		
		return join_lines (cmd)

	def install (self):
		gub.Cross_package.install (self)
		self.system ('''
(cd %(tooldir)s/lib && ln -s libgcc_s.1.dylib libgcc_s.dylib)
''')

	def package (self):
		
		self.system ('''
tar -C %(tooldir)s -zcf %(gub_uploads)s/%(name)s-%(version)s.%(platform)s.gub lib/
''')
	def sysinstall (self):
		self.system ('''
mkdir -p %(system_root)s/usr/
tar -C %(system_root)s/usr/ -zxf %(gub_uploads)s/%(name)s-%(version)s.%(platform)s.gub
''')


def get_packages (settings):
	return (
		Darwin_sdk (settings).with (version='', mirror=download.hw),
#		Odcctools (settings).with (version='20051031', mirror=download.opendarwin, format='bz2'),
		Odcctools (settings).with (version='20051122', mirror=download.opendarwin, format='bz2'),		
		Gcc (settings).with (version='4.0.2', format='bz2'),
		)		
