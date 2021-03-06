#!/usr/bin/env python
""" setup.py for kinbaku
"""

import os, sys, subprocess
import errno, shutil

from setuptools import setup, find_packages
from optparse import OptionParser

BASEDIR = os.path.dirname(os.path.realpath(__file__))

def boot(opts, *args, **options):
    """ """
    def do(things):
        """ """
        shell = subprocess.Popen( 'bash',
                                  cwd=BASEDIR, shell=True,
                                  universal_newlines=True,
                                  env=os.environ,
                                  stdout=sys.stderr,
                                  stderr=sys.stderr,
                                  stdin=subprocess.PIPE)
        shell.communicate(things)
        return shell.poll() == 0

    def die(message):
        """ """
        sys.stderr.write("=> ERROR: %s\n" % message)
        sys.exit(9000)

    def do_or_die(thing, message):
        """ """
        sys.stderr.write("::%s\n" % thing)
        return do(thing) or die(message)

    def pip_flags(flags=None):
        """ """
        flags = dict({'--download-cache': opts.down_cache,
                      '--build': opts.build_cache,},
                     **(flags or {}))
        machine=lambda acc, pair: acc + "%s=%s " % pair
        return reduce(machine, flags.items(), "").strip()

    sys.stderr.write("=> Making env {name}\n".format(name=opts.name))
    cmd = 'virtualenv --no-site-packages {name}'.format(name=opts.name)
    do_or_die(cmd, "Failed to virtualenv")

    sys.stderr.write("=> Installing reqs\n")
    cmd  = 'source {name}/bin/activate && '
    cmd += 'pip install -E {name} {flags} -r requirements.txt'
    cmd  = cmd.format(name=opts.name, flags=pip_flags())
    do_or_die(cmd, "Failed to install requirements")

    sys.stderr.write("=> Installing self\n")
    cmd = 'source {name}/bin/activate && python setup.py {arguments}'
    arguments = opts.develop and "develop" or "install"
    cmd = cmd.format(name=opts.name, arguments=arguments)
    do_or_die(cmd, "Failed to install self")

    sys.stderr.write("=> Copying etc\n")
    try:
        shutil.copytree('etc', os.path.join(opts.name, 'etc'))
    except OSError, e:
        if errno.errorcode[e.errno] == 'EEXIST':
            sys.stderr.write("   \=> already exists\n")
        else: raise
    if options.get('exit', False): exit(0)

if __name__=='__main__':
    os.chdir(BASEDIR)
    parser = OptionParser()

    kargs = dict() #dest='quiet', default=False, help="quiet")
    parser.add_option('--dist-dir', **kargs)
    parser.add_option('--egg-base', {})
    parser.add_option('-c','--single-version-externally-managed', {})
    parser.add_option('--install-headers', {})

    parser.add_option('--quiet', '-q', **dict(dest='quiet', default=False, help="quiet"))


    kargs = dict(dest='down_cache', default="/tmp/.cortex.pip_cache.down",
               help="Location of the download cache [default: /tmp/.cortex.pip_cache.down]")
    parser.add_option('--download', '-d', **kargs)

    kargs = dict(dest='build_cache', default="/tmp/.cortex.pip_cache.build",
                 help="Location of the build dir [default: /tmp/.cortex.pip_cache.build]")
    parser.add_option('--build', **kargs)

    kargs = dict(dest="develop", action='store_false', default=True,
                 help="Install cortex as a library instead of for development (symlink here)")
    parser.add_option("--permanent", '-p', **kargs)

    (options, args) = parser.parse_args()

    setup(
        name        ='kinbaku',
        version     = '.1',
        description = 'use cases for rope',
        author      = 'mattvonrocketstein, in the gmails',
        url         = 'one of these days',
        package_dir = {'': 'lib'},
        packages    = find_packages('lib'),
        entry_points = {
            'console_scripts': [
                'kinbaku = kinbaku.bin.kbk:entry',
            ],
        },
    )
