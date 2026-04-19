# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file LICENSE.rst or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION ${CMAKE_VERSION}) # this file comes with cmake

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-src")
  file(MAKE_DIRECTORY "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-src")
endif()
file(MAKE_DIRECTORY
  "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-build"
  "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix"
  "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/tmp"
  "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src/sqlite_amalgamation-populate-stamp"
  "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src"
  "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src/sqlite_amalgamation-populate-stamp"
)

set(configSubDirs Debug)
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src/sqlite_amalgamation-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src/sqlite_amalgamation-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
