import os
import re
import sys
import platform
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def run(self):
        try:
            out = subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError("CMake must be installed to build the following extensions: " +
                               ", ".join(e.name for e in self.extensions))

        if platform.system() == "Windows":
            cmake_version = LooseVersion(re.search(r'version\s*([\d.]+)', out.decode()).group(1))
            if cmake_version < '3.1.0':
                raise RuntimeError("CMake >= 3.1.0 is required on Windows")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        cmake_args = ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + extdir,
                      '-DPYTHON_EXECUTABLE=' + sys.executable]
        
        if os.getenv('CMAKE_TOOLCHAIN_FILE') is not None:
            cmake_args.append(['-DCMAKE_TOOLCHAIN_FILE=' + os.getenv('CMAKE_TOOLCHAIN_FILE')])
            print("USING TOOLCHAIN: %s" % (os.getenv('CMAKE_TOOLCHAIN_FILE')))
        
        cfg = 'Debug' if self.debug else 'Release'
        build_args = ['--config', cfg]

        if platform.system() == "Windows":
            cmake_args += ['-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}'.format(cfg.upper(), extdir)]
            if sys.maxsize > 2**32:
                cmake_args += ['-A', 'x64']
            build_args += ['--', '/m']
        else:
            cmake_args += ['-DCMAKE_BUILD_TYPE=' + cfg]
            build_args += ['--', '-j2']

        env = os.environ.copy()
        env['CXXFLAGS'] = '{} -DVERSION_INFO=\\"{}\\"'.format(env.get('CXXFLAGS', ''),
                                                              self.distribution.get_version())
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['cmake', ext.sourcedir] + cmake_args, cwd=self.build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=self.build_temp)

setup(
    name='pangolin',
    version='0.0.1',
    description='Python binding for lightweight 3D visualization library Pangolin.',
	url='https://github.com/uoip/pangolin',
	license='MIT',
	keywords'Pangolin, binding, OpenGL, 3D, visualization, Point Cloud',
    long_description="""This is a Python binding for c++ library Pangolin 
        (https://github.com/stevenlovegrove/Pangolin).
        Pangolin is a lightweight portable rapid development library for managing 
        OpenGL display / interaction and abstracting video input. At its heart is 
        a simple OpenGl viewport manager which can help to modularise 3D visualisation 
        without adding to its complexity, and offers an advanced but intuitive 3D navigation 
        handler. Pangolin also provides a mechanism for manipulating program variables through 
        config files and ui integration, and has a flexible real-time plotter for visualising 
        graphical data.""",
    ext_modules=[CMakeExtension('pangolin')],
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
)