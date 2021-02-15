from __future__ import with_statement
from subprocess import *
import gdb

class ReattachCommand (gdb.Command):
    """Reattaches the new instance of the previous process.
First argument is the name of executable (enough to specify the first time)"""

    def __init__ (self):
        self.lastFn = ''
        super (ReattachCommand, self).__init__ ("ra",
                                                       gdb.COMMAND_SUPPORT,
                                                       gdb.COMPLETE_FILENAME)

    def invoke (self, arg, from_tty):
        args = arg.split(' ')
        fn = args[0].strip()
        if len(fn) > 0:
            self.lastFn = fn
            
        if len(self.lastFn) == 0:
            print('You have to specify the name of the process (for pidof) for the first time (it will be cached for later)')
            return

        pid = -1
        try:
            pid = check_output(["pidof",self.lastFn]).strip()
        except CalledProcessError as e:
            if e.returncode == 1:
                print('Process not found :(')
                return 1
            else:
                raise e

        gdb.execute('attach ' + pid.decode())
        gdb.execute('c')

ReattachCommand()
