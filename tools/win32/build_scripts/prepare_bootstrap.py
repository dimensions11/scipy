import os
import subprocess
from os.path import join as pjoin, split as psplit, dirname, exists as pexists
import re

def build_sdist(chdir):
    cwd = os.getcwd()
    try:
        os.chdir(chdir)
        cmd = ["python", "setup.py", "sdist", "--format=zip"]
        subprocess.call(cmd)
    except Exception, e:
        raise RuntimeError("Error while executing cmd (%s)" % e)
    finally:
        os.chdir(cwd)

def get_svn_version(chdir):
    out = subprocess.Popen(['svn', 'info'], 
                           stdout = subprocess.PIPE, cwd = chdir).communicate()[0]
    r = re.compile('Revision: ([0-9]+)')
    svnver = None
    for line in out.split('\n'):
        m = r.match(line)
        if m:
            svnver = m.group(1)

    if not svnver:
        raise ValueError("Error while parsing svn version ?")

    return svnver

def get_scipy_version(chdir):
    version_file = pjoin(chdir, "scipy", "version.py")
    if not pexists(version_file):
        raise IOError("file %s not found" % version_file)

    fid = open(version_file, "r")
    vregex = re.compile("version\s*=\s*'(\d+)\.(\d+)\.(\d+)'")
    isrelregex = re.compile("release\s*=\s*True")
    isdevregex = re.compile("release\s*=\s*False")
    isdev = None
    version = None
    for line in fid.readlines():
        m = vregex.match(line)
        if m:
            version = [int(i) for i in m.groups()]
        if isrelregex.match(line):
            if isdev is None:
                isdev = False
            else:
                raise RuntimeError("isdev already set ?")
        if isdevregex.match(line):
            if isdev is None:
                isdev = True
            else:
                raise RuntimeError("isdev already set ?")
            
    verstr = ".".join([str(i) for i in version])
    if isdev:
        verstr += "dev"
    return verstr

if __name__ == '__main__':
    ROOT = os.path.join("..", "..", "..")
    print build_sdist(ROOT)
