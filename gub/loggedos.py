import misc
import subprocess
import sys
import os
import shutil

def system (logger, cmd, **kwargs):
    """Can't go through misc.py, since we want the output of the process.
    """

    ignore_errors = kwargs.get ('ignore_errors')
    logger.write_log ('invoking %s\n' % cmd, 'command')

    proc = subprocess.Popen (cmd,  bufsize=1, shell=True,
                             env=kwargs.get ('env'),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             close_fds=True)

    for line in proc.stdout:
        logger.write_log (line, 'output')
    proc.wait ()

    if proc.returncode:
        m = 'Command barfed: %(cmd)s\n' % locals ()
        if not ignore_errors:
            logger_interface.error (m)
            raise misc.SystemFailed (m)
        
    return proc.returncode


########
# logged aliases to misc.py
def logged_function(logger, function, *args, **kwargs):
    logger.write_log ('Running %s\n' % function.__name__, 'action')
    logger.write_log ('Running %s: %s\n' % (function.__name__, repr(args)), 'command')
    logger.write_log ('Running %s %s\n  %s\n' % (function.__name__, repr(args), repr(kwargs)), 'debug')

    function (*args, **kwargs)

currentmodule = sys.modules[__name__] #ugh
for name, func in {'read_file': misc.read_file,
             'dump_file': misc.dump_file,
             'shadow':misc.shadow,
             'chmod': os.chmod,
             'copy2': shutil.copy2,
             'read_pipe': misc.read_pipe}.items():

    def with_logging (func):
        return lambda logger, *args, **kwargs: logged_function(logger, func, *args, **kwargs)

    currentmodule.__dict__[name] = with_logging (func)

