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

        if os.path.exists(os.path.join(root, '.git')):
            if (call(["git", "submodule", "update", "--init", "--recursive"], cwd=root, stderr=STDOUT) != 0):
                raise RuntimeError("Could not init git submodule")

        dest = os.path.join("mbientlab", "bleat")
        if (platform.system() == 'Windows'):
            vs2017 = os.path.join(clibs, 'bleat', 'vs2017')
            if (call(["MSBuild.exe", "bleat.vcxproj", "/p:Platform=%s" % machine, "/p:Configuration=Release"], cwd=vs2017, stderr=STDOUT) != 0):
                raise RuntimeError("Failed to compile bleat.dll")

            dll = os.path.join(vs2017, "" if machine == "x86" else machine, "Release", "bleat.dll")
            move(dll, dest)
        elif (platform.system() == 'Linux'):
            bleat = os.path.join(clibs, 'bleat')
            if (call(["make", "-C", bleat, "-j%d" % (cpu_count())], cwd=root, stderr=STDOUT) != 0):
                raise RuntimeError("Failed to compile libbleat.so")

            so = os.path.join(bleat, 'dist', 'release', 'lib', machine)
            BleatBuild._move(so, dest, 'libbleat.so')

            blepp = os.path.join(bleat, 'deps', 'libblepp')
            BleatBuild._move(blepp, dest, 'libble++.so')
        else:
            raise RuntimeError("pybleat is not supported for the '%s' platform" % platform.system())

        build_py.run(self)

so_pkg_data = ['libbleat.so*', 'libble++.so*'] if platform.system() == 'Linux' else ['bleat.dll']
setup(
    name='bleat',
    packages=['mbientlab', 'mbientlab.bleat'],
    version='0.1.0',
    description='Python bindings for MbientLab\'s bleat library',
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    package_data={'mbientlab.bleat': so_pkg_data},
    include_package_data=True,
    url='https://github.com/mbientlab/pybleat',
    author='MbientLab',
    author_email="hello@mbientlab.com",
    cmdclass={
        'build_py': BleatBuild,
    },
    keywords = ['mbientlab', 'bluetooth le', 'native'],
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)
