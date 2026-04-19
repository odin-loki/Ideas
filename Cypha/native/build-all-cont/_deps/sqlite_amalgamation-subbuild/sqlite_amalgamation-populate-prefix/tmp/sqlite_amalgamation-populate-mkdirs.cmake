# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/mnt/c/Users/odinl/OneDrive/Desktop/Cypha/native/build-all-cont/_deps/sqlite_amalgamation-src"
  "/mnt/c/Users/odinl/OneDrive/Desktop/Cypha/native/build-all-cont/_deps/sqlite_amalgamation-build"
  "/mnt/c/Users/odinl/OneDrive/Desktop/Cypha/native/build-all-cont/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix"
  "/mnt/c/Users/odinl/OneDrive/Desktop/Cypha/native/build-all-cont/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/tmp"
  "/mnt/c/Users/odinl/OneDrive/Desktop/Cypha/native/build-all-cont/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src/sqlite_amalgamation-populate-stamp"
  "/mnt/c/Users/odinl/OneDrive/Desktop/Cypha/native/build-all-cont/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src"
  "/mnt/c/Users/odinl/OneDrive/Desktop/Cypha/native/build-all-cont/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src/sqlite_amalgamation-populate-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/mnt/c/Users/odinl/OneDrive/Desktop/Cypha/native/build-all-cont/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src/sqlite_amalgamation-populate-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/mnt/c/Users/odinl/OneDrive/Desktop/Cypha/native/build-all-cont/_deps/sqlite_amalgamation-subbuild/sqlite_amalgamation-populate-prefix/src/sqlite_amalgamation-populate-stamp${cfgdir}") # cfgdir has leading slash
endif()
