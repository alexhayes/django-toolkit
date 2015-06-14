from __future__ import absolute_import
import os
import sys
from tempfile import NamedTemporaryFile
from contextlib import contextmanager
from django.core.files.base import File
from django.conf import settings


@contextmanager
def smart_open(filename=None, mode='r', *args, **kwargs):
    if filename and filename != '-':
        fh = open(filename, mode, *args, **kwargs)
    elif '+' in mode:
        raise NotImplementedError("Mode '+' is not supported by smart_open.")
    elif 'a' in mode:
        raise NotImplementedError("Mode 'a' is not supported by smart_open.")
    elif 'w' in mode:
        fh = sys.stdout
    elif 'r' in mode:
        fh = sys.stdin

    try:
        yield fh
    finally:
        if fh is not sys.stdout and fh is not sys.stdin:
            fh.close()


@contextmanager
def tempfile(**kwargs):
    f = NamedTemporaryFile(**kwargs)
    yield f


@contextmanager
def tempfilename(**kwargs):
    """
    Reserve a temporary file for future use.

    This is useful if you want to get a temporary file name, write to it in the
    future and ensure that if an exception is thrown the temporary file is removed.
    """
    kwargs.update(delete=False)
    try:
        f = NamedTemporaryFile(**kwargs)
        f.close()
        yield f.name
    except Exception:
        if os.path.exists(f.name):
            # Ensure we clean up after ourself
            os.unlink(f.name)
        raise


class FileSystemFile(File):
    """
    A filesystem file that can be used with FileSystemStorage.
    """
    def __init__(self, file):
        super(FileSystemFile, self).__init__(file)

    def temporary_file_path(self):
        """
        Returns the full path of this file.
        """
        return self.file.name

    def close(self):
        try:
            return self.file.close()
        except OSError as e:
            if e.errno != 2:
                # Means the file was moved or deleted before the tempfile
                # could unlink it.  Still sets self.file.close_called and
                # calls self.file.file.close() before the exception
                raise


def makedirs(p):
    """
    A makedirs that avoids a race conditions for multiple processes attempting to create the same directory.
    """
    try:
        os.makedirs(p, settings.FILE_UPLOAD_PERMISSIONS)
    except OSError:
        # Perhaps someone beat us to the punch?
        if not os.path.isdir(p):
            # Nope, must be something else...
            raise
