# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install dash-project
#
# You can edit this file again by typing:
#
#     spack edit dash-project
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

import os
import platform 
import sys
from spack import *


class DashProject(CMakePackage):
    """DASH, the C++ Template Library for Distributed Data Structures with Support for Hierarchical Locality for HPC and Data-Driven Science.""" 
    
    homepage = "https://dash-project.org"
    url      = "https://github.com/dash-project/dash/releases/download/v0.3.0/dash-0.3.0.tar.gz"
    git      = "https://github.com/dash-project/dash.git"

    version('develop', branch='development')
    version('master', branch='master')

    version('0.3.0', sha256='78143a067c03e9e8045b102c25a18c33496bea63bdd923587ec4c4c76119ee12')
#    version('0.2.0', sha256='f0291ffcb939aa69cdc22e7c2ecbf27d38b762d0d7dab345bd3c9f872fbccd6f',
#            url="https://github.com/dash-project/dash/archive/dash-0.2.0.tar.gz") #Issue with Pthreads

    variant('mpi', default=True, description='+mpi')
    variant('cuda',    default=False, description='+cuda')
    variant('papi',    default=True, description='+papi')
    variant('numactl', default=True, description='+numactl')
    variant('hwloc',   default=True, description='+hwloc')
    variant('blas',    default=True, description='+blas')
    variant('lapack',  default=True, description='+lapack')
    variant('likwid',  default=True, description='+likwid')
    variant('hdf5',    default=False, description='+hdf5')
    variant('memkind', default=True, description='+memkind')
    variant('plasma',  default=False, description='+plasma')

    variant('cxxstd',
               default='11',
               values=('11', '14', '17'),
               multi=False,
               description='Use the specified C++ standard when building.')

    variant('build_type', default='RelWithDebInfo',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    filter_compiler_wrappers(
            'dash-mpicxx','dash-mpic++','dash-mpiCC',relative_root='bin')

    depends_on('ninja', type='build')
    depends_on('mpi@3.0',when='+mpi', type=('build', 'run'))
    depends_on('cuda',when='+cuda', type=('build', 'run'))
    depends_on('papi',when='+papi', type=('build', 'run'))
    depends_on('numactl',when='+numactl', type=('build', 'run'))
    depends_on('hwloc',when='+hwloc', type=('build', 'run'))
    depends_on('googletest',when='+googletest')
    depends_on('blas',when='+blas', type=('build', 'run'))
    depends_on('lapack',when='+lapack', type=('build', 'run'))
    depends_on('likwid',when='+likwid', type=('build', 'run'))
    depends_on('plasma',when='+plasma', type=('build', 'run'))
    depends_on('hdf5 cxx=True fortran=True szip=True threadsafe=True',when='+hdf5', type=('build', 'run'))
    depends_on('memkind',when='+memkind', type=('build', 'run'))


    patch('INSTALL_PREFIX-out.patch')


    def cmake_args(self):
        spec = self.spec
        args = []
        args.append('-DCMAKE_CXX_STANDARD={0}'.format(
                        spec.variants['cxxstd'].value))
        # Require standard at configure time to guarantee the
                # compiler supports the selected standard.
        args.append('-DCMAKE_CXX_STANDARD_REQUIRED=ON')

        return args

#    def setup_dependent_build_environment(self, env, dependent_spec):
#        env.set('MPICXX', spack_cxx)

    def setup_run_environment(self, env):
        env.set('DASH_ROOT', self.prefix)
        env.set('DASH_BASE', self.prefix)

#    @run_after('install')
#    def filter_compilers(self):
#        """Run after install to tell the configuration files and Makefiles
#        to use the compilers that Spack built the package with.
#        If this isn't done, they'll have CC and CXX set to Spack's generic
#        cc and c++. We want them to be bound to whatever compiler
#        they were built with."""
#
#        kwargs = {'ignore_absent': True, 'backup': False, 'string': True}
#                                                                    
#        filenames = [
#            self.get_sysconfigdata_name(), self.get_makefile_filename()
#        ]
#
#        filter_file(spack_cc,  self.compiler.cc,  *filenames, **kwargs)
#        if spack_cxx and self.compiler.cxx:
#            filter_file(spack_cxx, self.compiler.cxx, *filenames, **kwargs)
#    @run_after('install')
#    def symlink(self):
#        spec = self.spec
#        prefix = self.prefix


#        module.dashproject = Executable('dash-mpiCC')
#        module.dashproject = Executable('dash-mpic++')
#        module.dash-project = Executable('dash-mpicxx')
