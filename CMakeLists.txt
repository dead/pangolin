cmake_minimum_required(VERSION 3.1)
project(pangolinpy)

include(ExternalProject)

list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake_modules)
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(MediaFoundation REQUIRED)
find_package(GLEW)
find_package(PNG)
find_package(JPEG)

set(PANGOLIN_INSTALL_DIR ${CMAKE_BINARY_DIR}/PangolinInstall)

option(BUILD_EXTERN_GLEW    "Automatically download, build and compile GLEW" OFF)
option(BUILD_EXTERN_LIBPNG  "Automatically download, build and compile libpng" OFF)
option(BUILD_EXTERN_LIBJPEG "Automatically download, build and compile libjpeg" OFF)

if(NOT GLEW_FOUND)
	set(BUILD_EXTERN_GLEW ON)
endif()

if(NOT PNG_FOUND)
	set(BUILD_EXTERN_LIBPNG ON)
endif()

if(NOT GLEW_FOUND)
	set(BUILD_EXTERN_LIBJPEG ON)
endif()

if(_WIN_)
	option( MSVC_USE_STATIC_CRT  "Use static C Runtime with MSVC, /MT instead of /MD" ON)
	
	# Make sure there are no erroneous C Runtime flags
	list(APPEND FLAG_VARS
        CMAKE_CXX_FLAGS CMAKE_CXX_FLAGS_DEBUG CMAKE_CXX_FLAGS_RELEASE CMAKE_CXX_FLAGS_MINSIZEREL CMAKE_CXX_FLAGS_RELWITHDEBINFO
        CMAKE_C_FLAGS CMAKE_C_FLAGS_DEBUG CMAKE_C_FLAGS_RELEASE CMAKE_C_FLAGS_MINSIZEREL CMAKE_C_FLAGS_RELWITHDEBINFO
    )
	
	if(MSVC_USE_STATIC_CRT)
        foreach(FLAG_VAR ${FLAG_VARS})
            string(REGEX REPLACE "/MD" "/MT" NEW_FLAGS "${${FLAG_VAR}}")
            set(${FLAG_VAR} "${NEW_FLAGS}" CACHE STRING "" FORCE)
        endforeach()
    else()
        foreach(FLAG_VAR ${FLAG_VARS})
            string(REGEX REPLACE "/MT" "/MD" NEW_FLAGS "${${FLAG_VAR}}")
            set(${FLAG_VAR} "${NEW_FLAGS}" CACHE STRING "" FORCE)
        endforeach()
    endif()
endif()

ExternalProject_Add(
	_Pangolin
	GIT_REPOSITORY "https://github.com/stevenlovegrove/Pangolin.git"
	GIT_TAG "master"
	INSTALL_COMMAND
		cmake
		--build .
		--target install
		--config Release
	CMAKE_ARGS
		-DCMAKE_INSTALL_PREFIX=${PANGOLIN_INSTALL_DIR}
		-DBUILD_EXAMPLES=OFF
		-DBUILD_TESTS=OFF
		-DBUILD_EXTERN_GLEW=OFF
		-DBUILD_EXTERN_LIBPNG=OFF
		-DBUILD_EXTERN_LIBJPEG=OFF
		-DBUILD_PANGOLIN_GUI=ON
		-DMSVC_USE_STATIC_CRT=${MSVC_USE_STATIC_CRT}
		-DCMAKE_TOOLCHAIN_FILE=${CMAKE_TOOLCHAIN_FILE}
)

add_library(Pangolin STATIC IMPORTED GLOBAL)
add_dependencies(Pangolin _Pangolin)
set_target_properties(Pangolin PROPERTIES
    IMPORTED_LOCATION ${PANGOLIN_INSTALL_DIR}/lib/pangolin.lib
)

if(BUILD_EXTERN_GLEW)
	add_library(_glew STATIC IMPORTED GLOBAL)
	add_dependencies(_glew _Pangolin)
	
	set(GLEW_INCLUDE_DIR "${PANGOLIN_INSTALL_DIR}/include")
	set(GLEW_LIBRARY _glew)
	
	set_target_properties(_glew PROPERTIES
		IMPORTED_LOCATION_RELWITHDEBINFO ${PANGOLIN_INSTALL_DIR}/lib/glew.lib
		IMPORTED_LOCATION_RELEASE ${PANGOLIN_INSTALL_DIR}/lib/glew.lib
		IMPORTED_LOCATION_DEBUG   ${PANGOLIN_INSTALL_DIR}}/lib/glewd.lib
	)
endif()

if(BUILD_EXTERN_LIBPNG)
	add_library(_zlib STATIC IMPORTED GLOBAL)
	add_dependencies(_zlib _Pangolin)
	set_target_properties(_zlib PROPERTIES
		IMPORTED_LOCATION_RELEASE ${PANGOLIN_INSTALL_DIR}/lib/zlibstatic.lib
		IMPORTED_LOCATION_RELWITHDEBINFO ${PANGOLIN_INSTALL_DIR}/lib/zlibstatic.lib
		IMPORTED_LOCATION_DEBUG   ${PANGOLIN_INSTALL_DIR}/lib/zlibstaticd.lib
	)
	
	add_library(_libpng STATIC IMPORTED GLOBAL)
	add_dependencies(_libpng _Pangolin _zlib)
	set_target_properties(_libpng PROPERTIES
		IMPORTED_LOCATION_RELWITHDEBINFO ${PANGOLIN_INSTALL_DIR}/lib/libpng16_static.lib
		IMPORTED_LOCATION_RELEASE ${PANGOLIN_INSTALL_DIR}/lib/libpng16_static.lib
		IMPORTED_LOCATION_DEBUG   ${PANGOLIN_INSTALL_DIR}/lib/libpng16_staticd.lib
	)
	
	set(PNG_LIBRARY _libpng)
	set(ZLIB_LIBRARY _zlib)
endif()

if(BUILD_EXTERN_LIBJPEG)
	add_library(_libjpeg STATIC IMPORTED GLOBAL)
	add_dependencies(_libjpeg _Pangolin)
	set_target_properties(_libjpeg PROPERTIES
		IMPORTED_LOCATION ${PANGOLIN_INSTALL_DIR}/lib/jpeg.lib
	)
	set(JPEG_LIBRARY _libjpeg)
endif()

add_subdirectory(pybind11)

include_directories(${PANGOLIN_INSTALL_DIR}/include)
include_directories(${PROJECT_SOURCE_DIR}/src)
include_directories(${EIGEN3_INCLUDE_DIR})
include_directories(${OPENGL_INCLUDE_DIR})
include_directories(${GLEW_INCLUDE_DIR})

pybind11_add_module(pangolinpy src/pangolin.cpp)

target_link_libraries(pangolinpy PRIVATE
	${OPENGL_LIBRARIES}
	${GLEW_LIBRARY}
	${PNG_LIBRARY}
	${ZLIB_LIBRARY}
	${JPEG_LIBRARY}
	${MediaFoundation_LIBRARIES}
	Pangolin
)

add_dependencies(pangolinpy Pangolin)
