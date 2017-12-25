#!/usr/bin/env python3
import sys
import os

import glob


class InvalidConfigException(Exception):
    pass


class GlobalConfig(object):
    """
    The do* methods will run depending on the classes attribute without
    further checks
    """
    outdir = "" #directory to put everything or tar(.gz)(.gpg)
    name = "backup_%Y-%m-%d" #name of the directory or tar(.gz)(.gpg) without file suffixes
    logging = None #systemd or file or ?
    prerun = None #script to invoke
    postrun = None #script to invoke
    tar = True #tar everything at the end
    gzip = True #gzip? depends on cls.tar
    gpg = None #encrypt? recipient as string
    workspace = "" #temp directory
    preCleanWorkspace = True #clean workspace from prior runs
    postCleanWorkspace = True #clean workspace at the end

    @classmethod
    def load(cls, conf):
        pass

    @classmethod
    def save(cls, conf):
        pass

    @classmethod
    def validate(cls):
        if not os.path.isdir(cls.outdir):
            raise InvalidConfigException("%s is not a valid output dir"
                                         % cls.outdir)

        if not os.access(cls.outdir, os.W_OK):
            raise InvalidConfigException("%s is not writable" % cls.outdir)

    @classmethod
    def _doCleanWorkspace(cls):
        pass

    @classmethod
    def doPreClean(cls):
        if cls.preCleanWorkspace:
            cls._doCleanWorkspace()

    @classmethod
    def doPostClean(cls):
        if cls.postCleanWorkspace:
            cls._doCleanWorkspace()

    @classmethod
    def doPreRun(cls):
        pass

    @classmethod
    def doPostRun(cls):
        pass


class BackupPartial(object):
    def __init__(self, conf):
        pass

    def run(self):
        pass


def printUsage(execname):
    print("Usage: %s configdir" % execname)


def main(argv):
    execname = argv[0] if len(argv) > 1 else "cobrackup.py"

    if len(argv) != 2:
        printUsage(execname)
        sys.exit(1)

    confdir = argv[1]
    if not os.path.isdir(confdir):
        print("No such directory: %s" % confdir)
        printUsage(execname)
        sys.exit(1)

    globconf = os.path.join(confdir, "cobrackup.conf")
    if os.path.isfile(globconf):
        GlobalConfig.load(globconf)
    else:
        print("No cobrackup config found, a default but invalid one will be "
              "written to %s. Change it to your needs and re-run." % globconf)
        GlobalConfig.save(globconf)
        sys.exit(1)

    GlobalConfig.validate()

    partials = []
    for conf in glob.glob(os.path.join(confdir, "*.conf")):
        if os.path.basename(conf) != "cobrackup.conf":
            partials.append(BackupPartial(conf))

    GlobalConfig.doPreClean()
    GlobalConfig.doPreRun()

    for p in partials:
        p.run()

    GlobalConfig.doPostRun()
    GlobalConfig.doPostClean()


if __name__ == "__main__":
    main(sys.argv)
