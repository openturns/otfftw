

ot_add_current_dir_to_include_dirs ()

ot_add_source_file ( FFTW.cxx )

ot_install_header_file ( FFTW.hxx )

include_directories ( ${INTERNAL_INCLUDE_DIRS} )

add_library ( otfftw ${SOURCEFILES} )
if ( BUILD_SHARED_LIBS )
  set_target_properties ( otfftw PROPERTIES COMPILE_DEFINITIONS "OTFFTW_DLL_EXPORTS" )
endif ()

if ( NOT DEFINED LIB_VERSION ) 
  set ( LIB_VERSION 0.1.0 )
endif ()
if ( NOT DEFINED LIB_SOVERSION ) 
  set ( LIB_SOVERSION 0 )
endif ()
set_target_properties ( otfftw PROPERTIES VERSION ${LIB_VERSION} )
set_target_properties ( otfftw PROPERTIES SOVERSION ${LIB_SOVERSION} )
target_link_libraries ( otfftw ${OTFFTW_LIBRARIES} )
target_link_libraries ( otfftw ${OPENTURNS_LIBRARIES} )
target_link_libraries ( otfftw ${FFTW_LIBRARIES} )

if (NOT FFTW_FOUND)
  add_dependencies (otfftw fftw)
endif ()

install ( TARGETS otfftw
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION ${OTFFTW_LIBRARY_PATH}
  ARCHIVE DESTINATION ${OTFFTW_LIBRARY_PATH}
)

