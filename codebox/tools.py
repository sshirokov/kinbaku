""" kinbaku.tools:
      mostly copied from ropetest.testutils
"""

zam='bang'

import os.path
import shutil
import sys

import rope.base.project
from rope.contrib import generate
print random.choice
def sample_project(root=None, foldername=None, **kwds):
    if root is None:
        root = 'sample_project'
        if foldername:
            root = foldername
        # HACK: Using ``/dev/shm/`` for faster tests
        if os.name == 'posix' and os.path.isdir('/dev/shm'):
            root = '/dev/shm/' + root
    # Using these prefs for faster tests
    prefs = {'save_objectdb': False, 'save_history': False,
             'validate_objectdb': False, 'automatic_soa': False,
             'ignored_resources': ['.ropeproject', '*.pyc'],
             'import_dynload_stdmods': False}
    prefs.update(kwds)
    remove_recursively(root)
    project = rope.base.project.Project(root, **prefs)
    return project

create_module = generate.create_module
create_package = generate.create_package

def remove_project(project):
    project.close()
    remove_recursively(project.address)


def remove_recursively(path):
    import time
    # windows sometimes raises exceptions instead of removing files
    if os.name == 'nt' or sys.platform == 'cygwin':
          for i in range(12):
            try:
                _remove_recursively(path)
            except OSError, e:
                if e.errno not in (13, 16, 32):
                    raise
                time.sleep(0.3)
            else:
                break
    else:
        _remove_recursively(path)

zam='bang'

def _remove_recursively(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path):
        os.remove(path)
    else:
        shutil.rmtree(path)
