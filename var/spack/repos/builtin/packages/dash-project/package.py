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
    version('0.2.0', sha256='f0291ffcb939aa69cdc22e7c2ecbf27d38b762d0d7dab345bd3c9f872fbccd6f',
             url="https://github.com/dash-project/dash/archive/dash-0.2.0.tar.gz") 



    variant('mpi',default=True, description="Enable MPI for dash")
    variant('dart',default='mpi',
            values=('mpi','shmem','cuda','base'),
            multi=False,
            description="Use specifc dart backend.")

    variant('cxxstd',
               default='17',
               values=('11', '14', '17'),
               multi=False,
               description='Use the specified C++ standard when building.')

    variant('cstd',
               default='11',
               values=('11', '14', '17'),
               multi=False,
               description='Use the specified C standard when building.')

    variant('build_type', default='RelWithDebInfo',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    variant('build_generic',default=False, description="Build generic",)
    variant('environment_type',
            default='default',
            values=('default','other'),
            description="Environment type, extend valid values!",)

    variant('shared',default=True, description='Enable Shared Libs')
    variant('threads',default=False, description='Enable THREADSUPPORT using threads')
    variant('dev_compiler_warnings',default=False, description='Enable developer compiler warnings')
    variant('ext_compiler_warnings',default=False, description='Enable extended compiler warnings')
    variant('lt_optimization',default=False, description='lt optimization')
    variant('enable_assertions',default=False, description='enable assertions'),
    variant('shared_windows',default=True, description='enable shared windows'),
    variant('dynamic_windows',default=True, description='enable dynamic windows'),
    variant('default_index_type_long',default=True, description='set default index type to long'),
    variant('logging',default=False, description='enable logging'),
    variant('trace_logging',default=False, description='enable trace logging'),
    variant('dart_logging',default=False, description='enable dart logging'),

    variant('docs',default=True,description='Build docs'),
    variant('examples',default=True,description='Build examples'),
    variant('tests',default=True,description='Build tests'),

    variant('papi', default=True, description='+papi')
    variant('mkl', default=False, description='+mkl')
    variant('blas', default=False, description='+blas')
    variant('hwloc', default=True, description='+hwloc')
    variant('likwid', default=False, description='+likwid')
    variant('lapack', default=True, description='+lapack')
    variant('scalapack', default=True, description='+scalapack')
    variant('plasma', default=False, description='+plasma')
    variant('hdf5', default=False, description='+hdf5')
    variant('memkind', default=True, description='+memkind')
    variant('numactl', default=True, description='+numactl')
    variant('googletest', default=False, description='+googletest')

    variant('ipm',default=False,description='depend on IPM (not in spack yet')
    depends_on('ipm', when="+ipm", type=('run','link'))


    depends_on('binutils', type=('build','run'))
    depends_on('libtool', type=('build','run'))
    depends_on('cmake', type=('build','run'))
    depends_on('ninja', type=('build','run'))
#    depends_on('ncurses', type=('build','run'))
    depends_on('pkgconfig', type='build')
    
    depends_on('cuda',when='dart=cuda', type=('build', 'run'))
    depends_on('mpi@3.0',when='dart=mpi', type=('build', 'run'))
    depends_on('mpi@3.0',when='+mpi', type=('build', 'run'))
    depends_on('papi',when='+papi', type=('build', 'run'))
    depends_on('mkl',when='+mkl', type=('build', 'run'))
    depends_on('blas',when='+blas', type=('build', 'run'))
    depends_on('hwloc@:1.999',when='+hwloc', type=('build', 'run'))
    depends_on('likwid',when='+likwid', type=('build', 'run'))
    depends_on('lapack',when='+lapack', type=('build', 'run'))
    depends_on('netlib-scalapack',when='+scalapack', type=('build', 'run'))
    depends_on('plasma',when='+plasma', type=('build', 'run'))
    depends_on('hdf5 cxx=True fortran=True szip=True threadsafe=True',when='+hdf5', type=('build', 'run'))
    depends_on('memkind',when='+memkind', type=('build', 'run'))
    depends_on('numactl',when='+numactl', type=('build', 'run'))
    depends_on('googletest',when='+googletest',type=('build','link'))

    depends_on('python',type=('build','run'))
   
    filter_compiler_wrappers(
            'dash-mpicxx','dash-mpic++','dash-mpiCC',relative_root='bin')


    patch('INSTALL_PREFIX-out.patch')


    def cmake_args(self):
        spec = self.spec
        args = [
            '-DCMAKE_BUILD_TYPE={0}'.format(
                        spec.variants['build_type'].value),
            '-DBUILD_SHARED_LIBS={0}'.format(
                        spec.variants['shared'].value),
            '-DBUILD_GENERIC={0}'.format(
                        spec.variants['build_generic'].value), \
            '-DENVIRONMENT_TYPE={0}'.format(
                        spec.variants['environment_type'].value), \
            '-DDART_IMPLEMENTATIONS={0}'.format(
                        spec.variants['dart'].value) ,
            '-DENABLE_THREADSUPPORT={0}'.format(
                        spec.variants['threads'].value),
            '-DENABLE_DEV_COMPILER_WARNINGS={0}'.format(
                        spec.variants['dev_compiler_warnings'].value),
            '-DENABLE_EXT_COMPILER_WARNINGS={0}'.format(
                        spec.variants['ext_compiler_warnings'].value),
            '-DENABLE_LT_OPTIMIZATION={0}'.format(
                        spec.variants['lt_optimization'].value),
            '-DENABLE_ASSERTIONS={0}'.format(
                        spec.variants['enable_assertions'].value),
            '-DENABLE_SHARED_WINDOWS={0}'.format(
                        spec.variants['shared_windows'].value),
            '-DENABLE_DYNAMIC_WINDOWS={0}'.format(
                        spec.variants['dynamic_windows'].value),
             '-DENABLE_DEFAULT_INDEX_TYPE_LONG={0}'.format(
                        spec.variants['default_index_type_long'].value),
            '-DENABLE_LOGGING={0}'.format(
                        spec.variants['logging'].value),
            '-DENABLE_TRACE_LOGGING={0}'.format(
                        spec.variants['trace_logging'].value),
            '-DENABLE_DART_LOGGING={0}'.format(
                        spec.variants['dart_logging'].value),
            '-DENABLE_LIBNUMA={0}'.format(
                        spec.variants['dart_logging'].value),
            '-DENABLE_LIKWID={0}'.format(
                        spec.variants['dart_logging'].value),

            '-DENABLE_HWLOC={0}'.format(
                        spec.variants['hwloc'].value),
            '-DENABLE_PAPI={0}'.format(
                        spec.variants['papi'].value),
            '-DENABLE_MKL={0}'.format(
                        spec.variants['mkl'].value),
            '-DENABLE_BLAS={0}'.format(
                        spec.variants['blas'].value),
            '-DENABLE_LAPACK={0}'.format(
                        spec.variants['lapack'].value),
            '-DENABLE_SCALAPACK={0}'.format(
                        spec.variants['scalapack'].value),
            '-DENABLE_PLASMA={0}'.format(
                        spec.variants['plasma'].value),
            '-DENABLE_HDF5={0}'.format(
                        spec.variants['hdf5'].value),
            '-DENABLE_MEMKIND={0}'.format(
                        spec.variants['memkind'].value),

            '-DBUILD_DOCS={0}'.format(
                        spec.variants['docs'].value),
            '-DBUILD_EXAMPLES={0}'.format( 
                        spec.variants['examples'].value),
            '-DBUILD_TESTS={0}'.format(
                        spec.variants['tests'].value),

            '-DCMAKE_CXX_STANDARD_REQUIRED=ON',
            '-DCMAKE_EXPORT_COMPILE_COMMANDS=ON',
            '-DCMAKE_CXX_STANDARD={0}'.format(
                        spec.variants['cxxstd'].value),
            ]

        if '+mpi' in spec:
            args.extend([
                '-DDASH_IMPLEMENTATIUON_MPI_ENABLED={0}'.format(
                    self.spec['mpi'].prefix),
                ])
        if '+ipm' in spec:
            args.extend([
                '-DIPM_PREFIX={0}'.format(
                    self.spec['ipm'].prefix),
                '-DIPM_INCLUDE_DIRS={0}'.format(
                    self.spec['ipm'].prefix.include),
#                '-DIPM_LIBRARIES={0}'.format(
#                    self.spec['ipm'].prefix.lib),
                ])
        if '+numactl' in spec:
            args.extend([
                '-DNUMA_INCLUDE_DIRS={0}'.format(
                    self.spec['numactl'].prefix.include),
#                '-DNUMA_LIBRARIES={0}'.format(
#                    self.spec['numactl'].prefix.lib),
                ])

        if '+papi' in spec:
            args.extend([
                '-DPAPI_INCLUDE_DIRS={0}'.format(
                    self.spec['papi'].prefix.include),
#                '-DPAPI_LIBRARIES={0}'.format(
#                    self.spec['papi'].prefix.lib),
                '-DPAPI_PREFIX={0}'.format(
                    self.spec['papi'].prefix),
                ])

        if '+googletest' in spec:
            args.extend([
                '-DGTEST_INCLUDE_PATH={0}'.format(
                    self.spec['googletest'].prefix.include),
                '-DGTEST_LIBRARY_PATH={0}'.format(
                    self.spec['googletest'].prefix.lib)
                ])

        if '+hwloc' in spec:
            args.extend([
                '-DHWLOC_PREFIX={0}'.format(
                    self.spec['hwloc'].prefix),
                '-DHWLOC_INCLUDE_DIRS={0}'.format(
                    self.spec['hwloc'].prefix.include),
#                '-DHWLOC_LIBRARIES={0}'.format(
#                    self.spec['hwloc'].prefix.lib),
                ])

        if '+hdf5' in spec:
            args.extend([
                '-DHDF5_DIR={0}'.format(
                    self.spec['hdf5'].prefix),
                '-DHDF5_INCLUDE_DIRS={0}'.format(
                    self.spec['hdf5'].prefix.include),
#                '-DHDF5_LIBRARIES={0}'.format(
#                    self.spec['hdf5'].prefix.lib),
                ])

        if '+likwid' in spec:
            args.extend([
                '-DLIKWID_PREFIX={0}'.format(
                    self.spec['likwid'].prefix),
                '-DLIKWID_INCLUDE_DIRS={0}'.format(
                    self.spec['likwid'].prefix.include),
#                '-DLIKWID_LIBRARIES={0}'.format(
#                    self.spec['likwid'].prefix.lib),
                ])

        if '+memkind' in spec:
            args.extend([
                '-DMEMKIND_PREFIX={0}'.format(
                    self.spec['memkind'].prefix),
                '-DMEMKIND_INCLUDE_DIRS={0}'.format(
                    self.spec['memkind'].prefix.include),
#                '-DMEMKIND_LIBRARIES={0}'.format(
#                    self.spec['memkind'].prefix.lib),
            ])

        if '+plasma' in spec:
            args.extend([
                '-DPLASMA_INCLUDE_DIRS={0}'.format(
                    self.spec['plasma'].prefix.include),
#                '-DPLASMA_LIBRARIES={0}'.format(
#                    self.spec['plasma'].prefix.lib),
                '-DPLASMA_PREFIX={0}'.format(
                    self.spec['plasma'].prefix),
            ])

            #       if '+thread' in spec:
#            args.extend([
#                '-DTHREAD_LIBRARY={0}'.format(
#                    self.spec['pthread'].prefix.lib),
#                ])

        if '+scalapack' in spec:
            args.extend([
                '-DSCALAPACK_INCLUDE_DIRS={0}'.format(
                    self.spec['scalapack'].prefix.include),
#                '-DSCALAPACK_LIBRARIES={0}'.format(
#                    self.spec['scalapack'].prefix.lib),
#                '-DSCALAPACK_LIBRARY={0}'.format(
#                    self.spec['scalapack'].prefix.lib), #needs actual library not path!
            ])
        if '+mkl' in spec:
                '-DMKL_INCLUDE_DIR={0}'.format(
                    self.spec['mkl'].prefix.include),

        return args


    def setup_dependent_build_environment(self, env, dependent_spec):
        self.spec.mpicc = spack_cc
        self.spec.mpicxx = spack_cxx
        env.set('MPICC',spack_cc)
        env.set('MPICXX', spack_cxx)
        env.set('MPICC_CC', spack_cc)
        env.set('MPICXX_CXX', spack_cxx)

    def setup_run_environment(self, env):
        env.set('DASH_ROOT', self.prefix)

######## Parameters not set directly: according to cmake -LAH .
#BLACS_LIBRARY:FILEPATH=
#BLAS_mkl_intel_LIBRARY:FILEPATH=
#BLAS_mkl_intel_lp64_LIBRARY:FILEPATH=
#BLAS_mkl_intel_thread_LIBRARY:FILEPATH=
#BLAS_mkl_sequential_LIBRARY:FILEPATH=
#BUILD_COVERAGE_TESTS:BOOL=OFF
#CC_GDB_FLAG:STRING=-g
#CC_STD_FLAG:STRING=--std=c11
#CMAKE_ADDR2LINE:FILEPATH=
#CMAKE_AR:FILEPATH=
#CMAKE_COLOR_MAKEFILE:BOOL=ON
#CMAKE_CXX_COMPILER:FILEPATH=/usr/bin/c++
#CMAKE_CXX_COMPILER_AR:FILEPATH=/usr/bin/gcc-ar-9
#CMAKE_CXX_COMPILER_RANLIB:FILEPATH=/usr/bin/gcc-ranlib-9
#CMAKE_CXX_FLAGS:STRING=
#CMAKE_CXX_FLAGS_DEBUG:STRING=-g
#CMAKE_CXX_FLAGS_MINSIZEREL:STRING=-Os -DNDEBUG
#CMAKE_CXX_FLAGS_RELEASE:STRING=-O3 -DNDEBUG
#CMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING=-O2 -g -DNDEBUG
#CMAKE_C_COMPILER:FILEPATH=
#CMAKE_C_COMPILER_AR:FILEPATH=
#CMAKE_C_COMPILER_RANLIB:FILEPATH=
#CMAKE_C_FLAGS:STRING=
#CMAKE_C_FLAGS_DEBUG:STRING=-g
#CMAKE_C_FLAGS_MINSIZEREL:STRING=-Os -DNDEBUG
#CMAKE_C_FLAGS_RELEASE:STRING=-O3 -DNDEBUG
#CMAKE_C_FLAGS_RELWITHDEBINFO:STRING=-O2 -g -DNDEBUG
#CMAKE_DEBUG_POSTFIX:STRING=d
#CMAKE_DLLTOOL:FILEPATH=
#CMAKE_EXE_LINKER_FLAGS:STRING=
#CMAKE_EXE_LINKER_FLAGS_DEBUG:STRING=
#CMAKE_EXE_LINKER_FLAGS_MINSIZEREL:STRING=
#CMAKE_EXE_LINKER_FLAGS_RELEASE:STRING=
#CMAKE_EXE_LINKER_FLAGS_RELWITHDEBINFO:STRING=
#CMAKE_EXPORT_COMPILE_COMMANDS:BOOL=OFF
#CMAKE_LINKER:FILEPATH=
#CMAKE_MAKE_PROGRAM:FILEPATH=
#CMAKE_MODULE_LINKER_FLAGS:STRING=
#CMAKE_MODULE_LINKER_FLAGS_DEBUG:STRING=
#CMAKE_MODULE_LINKER_FLAGS_MINSIZEREL:STRING=
#CMAKE_MODULE_LINKER_FLAGS_RELEASE:STRING=
#CMAKE_MODULE_LINKER_FLAGS_RELWITHDEBINFO:STRING=
#CMAKE_NM:FILEPATH=
#CMAKE_OBJCOPY:FILEPATH=
#CMAKE_OBJDUMP:FILEPATH=
#CMAKE_RANLIB:FILEPATH=
#CMAKE_READELF:FILEPATH=
#CMAKE_SHARED_LINKER_FLAGS:STRING=
#CMAKE_SHARED_LINKER_FLAGS_DEBUG:STRING=
#CMAKE_SHARED_LINKER_FLAGS_MINSIZEREL:STRING=
#CMAKE_SHARED_LINKER_FLAGS_RELEASE:STRING=
#CMAKE_SHARED_LINKER_FLAGS_RELWITHDEBINFO:STRING=
#CMAKE_SKIP_INSTALL_RPATH:BOOL=NO
#CMAKE_SKIP_RPATH:BOOL=NO
#CMAKE_STATIC_LINKER_FLAGS:STRING=
#CMAKE_STATIC_LINKER_FLAGS_DEBUG:STRING=
#CMAKE_STATIC_LINKER_FLAGS_MINSIZEREL:STRING=
#CMAKE_STATIC_LINKER_FLAGS_RELEASE:STRING=
#CMAKE_STATIC_LINKER_FLAGS_RELWITHDEBINFO:STRING=
#CMAKE_STRIP:FILEPATH=
#CMAKE_VERBOSE_MAKEFILE:BOOL=FALSE
#CXX_GDB_FLAG:STRING=-g
#CXX_STD_FLAG:STRING=--std=c++14
#DASH_DART_BASE_INCLUDE_DIR:PATH=dash/dart-impl/base/include
#DASH_DART_IF_INCLUDE_DIR:PATH=dash/dart-if/include
#DASH_ENV_HOST_SYSTEM_ID:STRING=default
#DASH_PLATFORM_IS_POSIX:BOOL=TRUE
#DASH_PLATFORM_NAME:STRING=Linux
#DASH_VERSION:STRING=0.4.0
#DASH_VERSIONED_PROJECT_NAME:STRING=dash-0.4.0
#DASH_VERSION_MAJOR:STRING=0
#DASH_VERSION_MINOR:STRING=4
#DASH_VERSION_PATCH:STRING=0
#ENABLE_CC_REPORTS:BOOL=OFF
#ENABLE_COMPTIME_RED:BOOL=ON
#ENABLE_HWLOC_PCI:BOOL=ON
#ENABLE_NASTYMPI:BOOL=OFF
#ENABLE_TEST_LOGGING:BOOL=ON
#ENVIRONMENT_CONFIG_PATH:STRING=
#ENVIRONMENT_TYPE:STRING=default
#HDF5_C_COMPILER_EXECUTABLE:FILEPATH=
#HDF5_C_INCLUDE_DIR:PATH=
#HDF5_DIFF_EXECUTABLE:FILEPATH=
#HDF5_IS_PARALLEL:BOOL=FALSE
#HDF5_hdf5_LIBRARY_DEBUG:FILEPATH=
#HDF5_hdf5_LIBRARY_RELEASE:FILEPATH=
#HWLOC_LIBRARIES:FILEPATH=
#HWLOC_PREFIX:PATH=
#INSTALL_TESTS:BOOL=OFF
#IOMP5_LIBRARY:FILEPATH=
#IPM_LIBRARIES:FILEPATH=
#LIBCBLAS_LIBRARY:FILEPATH=
#LIKWID_LIBRARIES:FILEPATH=
#MATH_LIBRARY:FILEPATH=
#MEMKIND_LIBRARIES:FILEPATH=
#MKL_RT_LIBRARY:FILEPATH=
#MPIEXEC_EXECUTABLE:FILEPATH=
#MPIEXEC_MAX_NUMPROCS:STRING=4
#MPIEXEC_NUMPROC_FLAG:STRING=-n
#MPIEXEC_POSTFLAGS:STRING=
#MPIEXEC_PREFLAGS:STRING=
#MPI_CXX_ADDITIONAL_INCLUDE_DIRS:STRING=
#MPI_CXX_COMPILER:FILEPATH=
#MPI_CXX_COMPILE_DEFINITIONS:STRING=
#MPI_CXX_COMPILE_OPTIONS:STRING=-fexceptions;-pthread
#MPI_CXX_FLAGS:STRING=-DOMPI_SKIP_MPICXX
#MPI_CXX_HEADER_DIR:PATH=
#MPI_CXX_LIB_NAMES:STRING=mpi_cxx;mpi
#MPI_CXX_LINK_FLAGS:STRING=
#MPI_CXX_SKIP_FLAGS:STRING=-DOMPI_SKIP_MPICXX
#MPI_CXX_SKIP_MPICXX:BOOL=FALSE
#MPI_C_ADDITIONAL_INCLUDE_DIRS:STRING=
#MPI_C_COMPILER:FILEPATH=
#MPI_C_COMPILE_DEFINITIONS:STRING=
#MPI_C_COMPILE_OPTIONS:STRING=-fexceptions;-pthread
#MPI_C_HEADER_DIR:PATH=
#MPI_C_LIBRARIES:STRING=
#MPI_C_LIB_NAMES:STRING=mpi
#MPI_C_LINK_FLAGS:STRING=
#MPI_IMPL_ID:STRING=
#MPI_IMPL_IS_OPENMPI:BOOL=TRUE
#MPI_INCLUDE_PATH:STRING=
#MPI_IS_DART_COMPATIBLE:BOOL=TRUE
#MPI_LINK_FLAGS:STRING=
#MPI_mpi_LIBRARY:FILEPATH=
#MPI_mpi_cxx_LIBRARY:FILEPATH=
#NUMA_LIBRARIES:FILEPATH=
#OpenMP_CXX_FLAGS:STRING=-fopenmp
#OpenMP_CXX_LIB_NAMES:STRING=gomp;pthread
#OpenMP_C_FLAGS:STRING=-fopenmp
#OpenMP_C_LIB_NAMES:STRING=gomp;pthread
#OpenMP_gomp_LIBRARY:FILEPATH=
#OpenMP_pthread_LIBRARY:FILEPATH=
#PAPI_LIBRARIES:FILEPATH=
#PLASMA_LIBRARIES:FILEPATH=
#PTHREAD_LIBRARY:FILEPATH=
#PYTHON_EXECUTABLE:FILEPATH=
#SCALAPACK_LIBRARIES:FILEPATH=
#SCALAPACK_LIBRARY:FILEPATH=
#TESTCASES:STRING=*
#WARNINGS_AS_ERRORS:BOOL=OFF
#gtest_build_samples:BOOL=OFF
#gtest_build_tests:BOOL=OFF
#gtest_disable_pthreads:BOOL=OFF
#gtest_force_shared_crt:BOOL=OFF
#gtest_hide_internal_symbols:BOOL=OFF
