import sys

import elevate.elevate_util as elevate_util


class Elevate:
    def __init__(self, show_console=True, graphical=True, restore_cwd=True):
        self.show_console = show_console
        self.graphical = graphical
        self.restore_cwd = restore_cwd
        self._invoked_args = elevate_util._process_elevate_opts()

    def __call__(self):
        """
        Re-launch the current process with root/admin privileges

        When run as root, this function does nothing.

        When not run as root, this function replaces the current process
            (Linux, macOS) or creates a child process, waits, and
            exits (Windows).

        :param show_console: (Windows only) if True, show a new console for the
            child process. Ignored on Linux / macOS.
        :param graphical: (POSIX only) if True, attempt to use graphical
            programs (gksudo, etc). Ignored on Windows.
        :param restore_cwd: (POSIX only) if False, the calling process'
            previous working directory won't be restored after elevating.
            Currently ignored on Windows.
        """
        if sys.platform.startswith("win"):
            from elevate.windows import _elevate
        else:
            from elevate.posix import _elevate
        _elevate(self._invoked_args, self.show_console,
                 self.graphical, self.restore_cwd)
