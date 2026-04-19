# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file LICENSE.rst or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 4.3.1)

# Reject any attempt to use a toolchain file. We must not use one because
# we could be downloading it here. If the CMAKE_TOOLCHAIN_FILE environment
# variable is set, the cache variable will have been initialized from it.
unset(CMAKE_TOOLCHAIN_FILE CACHE)
unset(ENV{CMAKE_TOOLCHAIN_FILE})

# We name the project and the target for the ExternalProject_Add() call
# to something that will highlight to the user what we are working on if
# something goes wrong and an error message is produced.

project(sqlite_amalgamation-populate NONE)



include(ExternalProject)
ExternalProject_Add(sqlite_amalgamation-populate
                     "UPDATE_DISCONNECTED" "False" "DOWNLOAD_EXTRACT_TIMESTAMP" "TRUE" "EXTERNALPROJECT_INTERNAL_ARGUMENT_SEPARATOR" "URL" "https://sqlite.org/2024/sqlite-amalgamation-3470200.zip" "URL_HASH" "SHA256=aa73d8748095808471deaa8e6f34aa700e37f2f787f4425744f53fdd15a89c40" "SOURCE_SUBDIR" "sqlite-amalgamation-3470200"
                    SOURCE_DIR          "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-src"
                    BINARY_DIR          "C:/Users/odinl/OneDrive/Desktop/Cypha/native/build-windows-msvc/_deps/sqlite_amalgamation-build"
                    CONFIGURE_COMMAND   ""
                    BUILD_COMMAND       ""
                    INSTALL_COMMAND     ""
                    TEST_COMMAND        ""
                    USES_TERMINAL_DOWNLOAD  YES
                    USES_TERMINAL_UPDATE    YES
                    USES_TERMINAL_PATCH     YES
)


