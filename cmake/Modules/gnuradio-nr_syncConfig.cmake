find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_NR_SYNC gnuradio-nr_sync)

FIND_PATH(
    GR_NR_SYNC_INCLUDE_DIRS
    NAMES gnuradio/nr_sync/api.h
    HINTS $ENV{NR_SYNC_DIR}/include
        ${PC_NR_SYNC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_NR_SYNC_LIBRARIES
    NAMES gnuradio-nr_sync
    HINTS $ENV{NR_SYNC_DIR}/lib
        ${PC_NR_SYNC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-nr_syncTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_NR_SYNC DEFAULT_MSG GR_NR_SYNC_LIBRARIES GR_NR_SYNC_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_NR_SYNC_LIBRARIES GR_NR_SYNC_INCLUDE_DIRS)
