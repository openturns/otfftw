cmake_minimum_required (VERSION 3.13)

option ( BUILD_PYTHON                 "Build the python module for the library"                               ON )
option ( BUILD_DOC                    "Build the documentation"                                               ON )
option ( BUILD_SHARED_LIBS            "Build shared libraries"                                                ON )

# By default, build in Release mode. Must appear before project() command
set( CMAKE_BUILD_TYPE Release CACHE STRING "Build type")

project (otfftw)

string (TOLOWER ${CMAKE_PROJECT_NAME} PACKAGE_NAME)

# set module dir to find custom scripts
list (APPEND CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

if (POLICY CMP0042)
  # MACOSX_RPATH is enabled by default
  cmake_policy(SET CMP0042 NEW)
endif()
if (POLICY CMP0078)
  # UseSWIG generates standard target names
  cmake_policy(SET CMP0078 NEW)
endif()
if (POLICY CMP0086)
  # UseSWIG honors SWIG_MODULE_NAME via -module flag
  cmake_policy(SET CMP0086 NEW)
endif()

find_package (OpenTURNS CONFIG REQUIRED)
message (STATUS "Found OpenTURNS: ${OPENTURNS_ROOT_DIR} (found version \"${OPENTURNS_VERSION_STRING}\")")
if (NOT DEFINED OPENTURNS_PYTHON_MODULE_PATH)
  set (OPENTURNS_PYTHON_MODULE_PATH ${OPENTURNS_PYTHON3_MODULE_PATH})
endif ()

find_package (FFTW REQUIRED)
list (APPEND OTFFTW_INCLUDE_DIRS ${FFTW_INCLUDE_DIRS})
list (APPEND OTFFTW_LIBRARIES ${FFTW_LIBRARIES})
list (APPEND OTFFTW_LIBRARY_DIRS ${FFTW_LIBRARY_DIRS})
include_directories(${FFTW_INCLUDE_DIRS})

set ( OTFFTW_DEFINITIONS ${OPENTURNS_DEFINITIONS} )
if (NOT BUILD_SHARED_LIBS)
  list ( APPEND OTFFTW_DEFINITIONS "-DOTFFTW_STATIC" )
endif ()
add_definitions ( ${OTFFTW_DEFINITIONS} )

if (NOT DEFINED CMAKE_INSTALL_LIBDIR)
  set (CMAKE_INSTALL_LIBDIR lib${LIB_SUFFIX})
endif ()

set (OTFFTW_LIBRARY_PATH ${CMAKE_INSTALL_LIBDIR})
set (OTFFTW_INCLUDE_PATH include)
set (OTFFTW_SWIG_INCLUDE_DIRS ${OTFFTW_INCLUDE_PATH}/${PACKAGE_NAME}/swig)
set (OTFFTW_DATA_PATH share)
set (OTFFTW_CONFIG_CMAKE_PATH ${CMAKE_INSTALL_LIBDIR}/cmake/otfftw)
set (OTFFTW_DOC_PATH share/${PACKAGE_NAME}/doc)

set (CMAKE_CXX_STANDARD 11)

if (BUILD_PYTHON)
  find_package (SWIG 3)
  include (${SWIG_USE_FILE})

  if (CMAKE_VERSION VERSION_LESS 3.24)
    find_package (Python 3.5 COMPONENTS Interpreter Development)
  else ()
    find_package (Python 3.5 COMPONENTS Interpreter Development.Module)
  endif ()

  if (Python_FOUND)
	  #include (FindPythonModule)
    if (NOT TARGET Python::Module)
      include (TargetLinkLibrariesWithDynamicLookup)
    endif ()

    if (USE_SPHINX)
      find_program (SPHINX_EXECUTABLE NAMES sphinx-build DOC "Sphinx Documentation Builder (sphinx-doc.org)")
      find_python_module (numpydoc)
      if (SPHINX_EXECUTABLE AND NUMPYDOC_FOUND)
        find_python_module (sphinx 1.1)
      endif ()
      if (NOT SPHINX_FOUND)
        message (STATUS "Disabling documentation (need sphinx/pandoc/numpydoc)")
      endif ()
    endif ()

    if (DEFINED PYTHON_SITE_PACKAGES)
      set (OTFFTW_PYTHON_MODULE_PATH "${PYTHON_SITE_PACKAGES}")
    else ()
     if (WIN32)
       set (OTFFTW_PYTHON_MODULE_PATH Lib/site-packages)
     else ()
       set (OTFFTW_PYTHON_MODULE_PATH ${CMAKE_INSTALL_LIBDIR}/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/site-packages)
      endif ()
    endif ()
  endif ()
endif ()


# Define variables without OTFFTW_ prefix with absolute paths
foreach (_var PYTHON_MODULE_PATH LIBRARY_PATH INCLUDE_PATH CONFIG_CMAKE_PATH)
  if (IS_ABSOLUTE "${OTFFTW_${_var}}")
    set (${_var} ${OTFFTW_${_var}})
  else ()
    set (${_var} ${CMAKE_INSTALL_PREFIX}/${OTFFTW_${_var}})
  endif ()
  get_filename_component (${_var} "${${_var}}" ABSOLUTE)
  file (TO_NATIVE_PATH "${${_var}}" NATIVE_${_var})
  string (REPLACE "\\" "\\\\" NATIVE_${_var} ${NATIVE_${_var}})
endforeach ()

# RPATH settings
set (CMAKE_INSTALL_RPATH ${LIBRARY_PATH})
set (CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# Some useful macros to ease CMakeLists.txt file writing
set (SOURCEFILES "" CACHE INTERNAL "List of source files to compile")
macro (ot_add_source_file FILENAME)
  set (sf ${SOURCEFILES} ${CMAKE_CURRENT_SOURCE_DIR}/${FILENAME})
  set (SOURCEFILES ${sf} CACHE INTERNAL "List of source files to compile")
endmacro ()

macro (ot_install_header_file FILENAME)
  install (FILES ${PACKAGE_NAME}/${FILENAME} DESTINATION ${OTFFTW_INCLUDE_PATH}/${PACKAGE_NAME})
endmacro ()

macro (ot_install_swig_file FILENAME)
  install (FILES ${FILENAME} DESTINATION ${OTFFTW_SWIG_INCLUDE_DIRS})
endmacro ()

set ( INTERNAL_INCLUDE_DIRS "" CACHE INTERNAL "List of directories with header files needed for build" )
macro ( ot_add_current_dir_to_include_dirs )
  set ( inc_dirs ${INTERNAL_INCLUDE_DIRS} ${CMAKE_CURRENT_SOURCE_DIR} )
  set ( INTERNAL_INCLUDE_DIRS ${inc_dirs} CACHE INTERNAL "List of directories with header files needed for build" )
endmacro ( ot_add_current_dir_to_include_dirs )


set ( CPACK_PACKAGE_NAME          ${PACKAGE_NAME} )
set ( CPACK_PACKAGE_VERSION_MAJOR 0              )
set ( CPACK_PACKAGE_VERSION_MINOR 12              )
set ( CPACK_PACKAGE_VERSION_PATCH                )
set ( CPACK_SOURCE_GENERATOR      "TGZ;TBZ2"     )
set (CPACK_BINARY_STGZ    OFF CACHE BOOL "STGZ")
set (CPACK_BINARY_TBZ2    ON  CACHE BOOL "TBZ2")
set (CPACK_BINARY_TGZ     ON  CACHE BOOL "TGZ" )
set (CPACK_BINARY_TZ      OFF CACHE BOOL "TZ"  )
set ( CPACK_SOURCE_IGNORE_FILES "/.git;/build;.*~;${CPACK_SOURCE_IGNORE_FILES}" )
set ( PACKAGE_NAME           ${CPACK_PACKAGE_NAME} )
set ( PACKAGE_VERSION        ${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR} )
if ( CPACK_PACKAGE_VERSION_PATCH )
  set ( PACKAGE_VERSION       ${PACKAGE_VERSION}.${CPACK_PACKAGE_VERSION_PATCH} )
endif ()
set ( CPACK_SOURCE_PACKAGE_FILE_NAME ${PACKAGE_NAME}-${PACKAGE_VERSION} )


# The tests can't be run if this function is absent
enable_testing ()
add_custom_target (tests COMMENT "Build tests")
add_custom_target (check COMMENT "Run pre-installation tests")
add_custom_target (installcheck COMMENT "Run post-installation tests")

add_subdirectory (lib)
add_dependencies (check cppcheck)

if (Python_FOUND AND SWIG_FOUND)
  add_subdirectory (python)
  add_dependencies (installcheck pyinstallcheck)
endif ()

if (BUILD_DOC)
  add_subdirectory (doc)
endif ()

# uninstall target
configure_file (
  ${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
  IMMEDIATE @ONLY
)

add_custom_target ( uninstall
  COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake_uninstall.cmake
)

set ( OTFFTW_LIBRARY                 otfftw )
set ( OTFFTW_LIBRARIES ${OPENTURNS_LIBRARIES} )
list ( APPEND OTFFTW_LIBRARIES ${OTFFTW_LIBRARY} )
set ( OTFFTW_LIBRARY_DIRS ${OPENTURNS_LIBRARY_DIRS} )
list ( APPEND OTFFTW_LIBRARY_DIRS ${LIBRARY_PATH} )
set ( OTFFTW_INCLUDE_DIR ${INCLUDE_PATH} )
set ( OTFFTW_INCLUDE_DIRS ${OTFFTW_INCLUDE_DIR} )
set ( OTFFTW_ROOT_DIR       ${CMAKE_INSTALL_PREFIX} )
list ( APPEND OTFFTW_INCLUDE_DIRS ${OPENTURNS_INCLUDE_DIRS} )
set ( OTFFTW_VERSION_STRING ${PACKAGE_VERSION} )
set ( OTFFTW_VERSION_MAJOR ${CPACK_PACKAGE_VERSION_MAJOR} )
set ( OTFFTW_VERSION_MINOR ${CPACK_PACKAGE_VERSION_MINOR} )
set ( OTFFTW_VERSION_PATCH ${CPACK_PACKAGE_VERSION_PATCH} )

include(CMakePackageConfigHelpers)
configure_package_config_file (cmake/otfftwConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/otfftwConfig.cmake
  INSTALL_DESTINATION ${OTFFTW_CONFIG_CMAKE_PATH}
  PATH_VARS
    OTFFTW_ROOT_DIR
    OTFFTW_INCLUDE_DIR
    OTFFTW_INCLUDE_DIRS
    OTFFTW_LIBRARY_DIRS
    PYTHON_MODULE_PATH
  NO_CHECK_REQUIRED_COMPONENTS_MACRO)

write_basic_package_version_file (otfftwConfigVersion.cmake VERSION ${OTFFTW_VERSION_STRING} COMPATIBILITY AnyNewerVersion)

install (FILES ${CMAKE_CURRENT_BINARY_DIR}/otfftwConfig.cmake
               ${CMAKE_CURRENT_BINARY_DIR}/otfftwConfigVersion.cmake
         DESTINATION ${OTFFTW_CONFIG_CMAKE_PATH})

include (CPack)
