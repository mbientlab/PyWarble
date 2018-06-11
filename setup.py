from distutils.dir_util import copy_tree
from multiprocessing import cpu_count
from shutil import move 
from subprocess import call, STDOUT
from setuptools import setup
from setuptools.command.build_py import build_py

import os
import platform
import sys

machine = "arm" if "arm" in platform.machine() else ("x64" if sys.maxsize > 2**32 else "x86")

class BleatBuild(build_py):
    @staticmethod
    def _move(src, dest, basename):
        for f in os.listdir(src):
            if (f.startswith(basename)):
                move(os.path.join(src, f), dest)

    def run(self):
        root = os.path.dirname(os.path.abspath(__file__))
        clibs = os.path.join(root, 'clibs')
        warble = os.path.join(clibs, 'warble')
        version_mk = os.path.join(warble, "version.mk")

        if os.path.exists(os.path.join(root, '.git')):
            if (call(["git", "submodule", "update", "--init", "--recursive"], cwd=root, stderr=STDOUT) != 0):
                raise RuntimeError("Could not init git submodule")

        dest = os.path.join("mbientlab", "warble")
        if (platform.system() == 'Windows'):
            args = ["MSBuild.exe", "warble.vcxproj", "/p:Platform=%s" % machine, "/p:Configuration=Release"]
            if (os.path.exists(version_mk)):
                args.append("/p:SkipVersion=1")

            vs2017 = os.path.join(warble, 'vs2017')
            if (call(args, cwd=vs2017, stderr=STDOUT) != 0):
                raise RuntimeError("Failed to compile warble.dll")

            dll = os.path.join(vs2017, "" if machine == "x86" else machine, "Release", "warble.dll")
            move(dll, dest)
        elif (platform.system() == 'Linux'):
            args = ["make", "-C", warble, "-j%d" % (cpu_count())]
            if (os.path.exists(version_mk)):
                args.append("SKIP_VERSION=1")

            if (call(args, cwd=root, stderr=STDOUT) != 0):
                raise RuntimeError("Failed to compile libwarble.so")

            so = os.path.join(warble, 'dist', 'release', 'lib', machine)
            BleatBuild._move(so, dest, 'libwarble.so')

            blepp = os.path.join(warble, 'deps', 'libblepp')
            BleatBuild._move(blepp, dest, 'libble++.so')
        else:
            raise RuntimeError("pywarble is not supported for the '%s' platform" % platform.system())

        build_py.run(self)

so_pkg_data = ['libwarble.so*', 'libble++.so*'] if platform.system() == 'Linux' else ['warble.dll']
setup(
    name='warble',
    packages=['mbientlab', 'mbientlab.warble'],
    version='1.0.0',
    description='Python bindings for MbientLab\'s Warble library',
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    package_data={'mbientlab.warble': so_pkg_data},
    include_package_data=True,
    url='https://github.com/mbientlab/PywWrble',
    author='MbientLab',
    author_email="hello@mbientlab.com",
    cmdclass={
        'build_py': BleatBuild,
    },
    keywords = ['mbientlab', 'bluetooth le', 'native'],
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 5 - Stable',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)
