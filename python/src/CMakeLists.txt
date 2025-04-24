
add_definitions (${OPENTURNS_SWIG_DEFINITIONS})

# allows one to pass compile flags like -O1 to reduce memory usage
set (SWIG_COMPILE_FLAGS "" CACHE STRING "C++ compiler flags used for wrapper code")

macro (ot_add_python_module MODULENAME SOURCEFILE)
  set_source_files_properties (${SOURCEFILE} PROPERTIES CPLUSPLUS ON)
  set_source_files_properties (${SOURCEFILE} PROPERTIES SWIG_MODULE_NAME ${MODULENAME})
  set_source_files_properties (${SOURCEFILE} PROPERTIES INCLUDE_DIRECTORIES "${INTERNAL_INCLUDE_DIRS};${OPENTURNS_INCLUDE_DIRS};${OPENTURNS_SWIG_INCLUDE_DIRS}")

  ot_install_swig_file (${SOURCEFILE})
  if (${ARGC} GREATER 2)
    set (SWIG_MODULE_${MODULENAME}_python_EXTRA_DEPS ${ARGN})
  endif ()

  set (swig_other_sources)
  foreach (it ${ARGN})
    if (${it} MATCHES ".*\\.i$")
      ot_install_swig_file (${it})
    else ()
      list (APPEND swig_other_sources "${it}")
    endif ()
  endforeach ()

  set (module_target ${MODULENAME}_python)

  swig_add_library (${module_target} LANGUAGE python SOURCES ${SOURCEFILE} ${swig_other_sources})

  target_include_directories(${module_target} PRIVATE ${INTERNAL_INCLUDE_DIRS})

  target_link_libraries (${module_target} otfftw)
  target_link_libraries (${module_target} Python::Module)

  set_target_properties (${module_target} PROPERTIES OUTPUT_NAME ${MODULENAME})
  set_target_properties (${module_target} PROPERTIES COMPILE_FLAGS "${SWIG_COMPILE_FLAGS}")
  set_target_properties (${module_target} PROPERTIES UNITY_BUILD OFF)

  install (FILES ${CMAKE_CURRENT_BINARY_DIR}/${MODULENAME}.py
           DESTINATION ${OTFFTW_PYTHON_MODULE_PATH}/${PACKAGE_NAME})
  install (TARGETS ${module_target}
            LIBRARY DESTINATION ${OTFFTW_PYTHON_MODULE_PATH}/${PACKAGE_NAME})

  list (APPEND OTFFTW_PYTHON_MODULES ${MODULENAME})
endmacro ()


ot_add_python_module ( ${PACKAGE_NAME} ${PACKAGE_NAME}_module.i FFTW.i )



install ( FILES __init__.py
          DESTINATION ${OTFFTW_PYTHON_MODULE_PATH}/${PACKAGE_NAME}
        )

# wheel files
configure_file (METADATA.in METADATA @ONLY)
install (FILES ${CMAKE_CURRENT_BINARY_DIR}/METADATA
	DESTINATION ${OTFFTW_PYTHON_MODULE_PATH}/${PACKAGE_NAME}-${PACKAGE_VERSION}.dist-info)
