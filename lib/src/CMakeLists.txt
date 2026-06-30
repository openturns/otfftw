ot_add_current_dir_to_include_dirs ()

ot_add_source_file (FFTW.cxx)

ot_install_header_file (FFTW.hxx)

include_directories (${INTERNAL_INCLUDE_DIRS})

add_library (otfftw ${SOURCEFILES})
if (BUILD_SHARED_LIBS)
  set_target_properties (otfftw PROPERTIES COMPILE_DEFINITIONS "OTFFTW_DLL_EXPORTS")
endif ()

if (NOT DEFINED LIB_VERSION)
  set (LIB_VERSION 0.0.0)
endif ()
if (NOT DEFINED LIB_SOVERSION)
  set (LIB_SOVERSION 0)
endif ()
set_target_properties (otfftw PROPERTIES VERSION ${LIB_VERSION})
set_target_properties (otfftw PROPERTIES SOVERSION ${LIB_SOVERSION})
target_link_libraries (otfftw ${OPENTURNS_LIBRARY})
target_link_libraries (otfftw ${FFTW_LIBRARIES})

# Add targets to the build-tree export set
export (TARGETS otfftw FILE ${PROJECT_BINARY_DIR}/OTFFTW-Targets.cmake)

# Install the export set for use with the install-tree
install (EXPORT OTFFTW-Targets
         DESTINATION "${OTFFTW_CONFIG_CMAKE_PATH}"
         COMPONENT Development)

install (TARGETS otfftw
         EXPORT  OTFFTW-Targets
         RUNTIME DESTINATION bin
         LIBRARY DESTINATION ${OTFFTW_LIBRARY_PATH}
         ARCHIVE DESTINATION ${OTFFTW_LIBRARY_PATH})
