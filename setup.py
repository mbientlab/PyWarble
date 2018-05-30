from distutils.dir_util import copy_tree
from multiprocessing import cpu_count
from shutil import copy2
from subprocess import call, STDOUT
from setuptools import setup
from setuptools.command.build_py import build_py

import os
import platform
import sys

machine = "arm" if "arm" in platform.machine() else ("x64" if sys.maxsize > 2**32 else "x86")

class BleatBuild(build_py):
    def run(self):
        root = os.path.dirname(os.path.abspath(__file__))

        if os.path.exists(os.path.join(root, '.git')):
            status = call(["git", "submodule", "update", "--init", "--recursive"], cwd=root, stderr=STDOUT)
            if (status != 0):
                raise RuntimeError("Could not init git submodule")

        status = call(["make", "-C", "bleat", "-j%d" % (cpu_count())], cwd=root, stderr=STDOUT)
        if (status != 0):
            raise RuntimeError("Failed to compile libbleat")

        copy_tree('bleat/dist/release/lib/%s/' % (machine), "mbientlab/bleat")
        copy2('bleat/deps/libblepp/libble++.so', "mbientlab/bleat")
        copy2('bleat/deps/libblepp/libble++.so.0', "mbientlab/bleat")
        copy2('bleat/deps/libblepp/libble++.so.0.5', "mbientlab/bleat")

        build_py.run(self)

setup(
    name='bleat',
    packages=['mbientlab', 'mbientlab.bleat'],
    version='0.1.0',
    description='Python bindings for MbientLab\'s bleat library',
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read(),
    package_data={'mbientlab.bleat': ['libbleat.so*']},
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
