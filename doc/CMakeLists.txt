
find_package ( LATEX )
set ( IMAGEMAGICK_CONVERT convert )
set ( LATEX2HTML_CONVERTER latex2html )
include ( UseLATEX )

# latex part 
if ( PDFLATEX_COMPILER AND BIBTEX_COMPILER )

  if ( ${CMAKE_CURRENT_BINARY_DIR} STREQUAL ${CMAKE_CURRENT_SOURCE_DIR} )
    # in-source build
    set ( LATEX_OUTPUT_PATH ${CMAKE_CURRENT_SOURCE_DIR}/build )
#     execute_process (
#       COMMAND ${CMAKE_COMMAND} -E create_symlink ${CMAKE_SOURCE_DIR}/src/logoOpenTURNS.jpg ${CMAKE_CURRENT_SOURCE_DIR}/logoOpenTURNS.jpg
#     )  
  else ()
    # out-of-source build
    set ( LATEX_OUTPUT_PATH ${CMAKE_CURRENT_BINARY_DIR} )
  endif ()
  add_latex_document ( otfftw_Documentation.tex
    INPUTS logootfftw.png GenericInformation.tex.in otfftw_summary.tex otfftw_UserManual.tex Math_Notations.sty otfftw_ExamplesGuide.tex otfftw_title.tex otfftw_Documentation.sty otfftw_ReferenceGuide.tex otfftw_UseCasesGuide.tex fftw_DSPEstimation.py UC1_transform.py UC2_spectral.py UC3_Welch.py DSPComparison.pdf
    DEFAULT_PDF
    MANGLE_TARGET_NAMES
  ) 

  configure_file( ${CMAKE_CURRENT_SOURCE_DIR}/GenericInformation.tex.in 
                  ${LATEX_OUTPUT_PATH}/GenericInformation.tex
                  @ONLY
  )
  
#   execute_process (
#     COMMAND ${CMAKE_COMMAND} -E create_symlink ${CMAKE_SOURCE_DIR}/latex2html/latex2html.sty ${LATEX_OUTPUT_PATH}/latex2html.sty
#     COMMAND ${CMAKE_COMMAND} -E create_symlink ${CMAKE_SOURCE_DIR}/src/Math_Notations.sty ${LATEX_OUTPUT_PATH}/Math_Notations.sty
#     COMMAND ${CMAKE_COMMAND} -E create_symlink ${CMAKE_BINARY_DIR}/src/GenericInformation.tex ${LATEX_OUTPUT_PATH}/GenericInformation.tex
#   )     
install ( FILES ${LATEX_OUTPUT_PATH}/otfftw_Documentation.pdf DESTINATION ${OTFFTW_DATA_PATH}/doc/pdf )

endif ()
