
add_subdirectory ( include )
add_subdirectory ( src )
add_subdirectory ( test )

install ( FILES ${HEADERFILES}
          DESTINATION ${OTFFTW_INCLUDE_PATH}/${PACKAGE_NAME}
        )

