# Copyright (C) 2018-2019 Intel Corporation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#      http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set(TARGET_NAME "multi_channel_human_pose_estimation_demo")

if(MULTICHANNEL_DEMO_USE_NATIVE_CAM OR MULTICHANNEL_DEMO_USE_TBB)
    set(CMAKE_CXX_STANDARD 14)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()

if( BUILD_DEMO_NAME AND NOT ${BUILD_DEMO_NAME} STREQUAL ${TARGET_NAME} )
    message(STATUS "DEMO ${TARGET_NAME} SKIPPED")
    return()
endif()

# Find OpenCV components if exist
find_package(OpenCV COMPONENTS highgui QUIET)
if(NOT(OpenCV_FOUND))
    message(WARNING "OPENCV is disabled or not found, " ${TARGET_NAME} " skipped")
    return()
endif()

file(GLOB MAIN_SRC ${CMAKE_CURRENT_SOURCE_DIR}/*.cpp)
file(GLOB MAIN_HEADERS ${CMAKE_CURRENT_SOURCE_DIR}/*.hpp)

# Create named folders for the sources within the .vcproj
# Empty name lists them directly under the .vcproj
source_group("src" FILES ${MAIN_SRC})
source_group("include" FILES ${MAIN_HEADERS})

# Create library file from sources.
add_executable(${TARGET_NAME} ${MAIN_SRC} ${MAIN_HEADERS})

set_target_properties(${TARGET_NAME} PROPERTIES COMPILE_PDB_NAME ${TARGET_NAME})

target_link_libraries(${TARGET_NAME} PRIVATE
    ${InferenceEngine_LIBRARIES} gflags ${OpenCV_LIBRARIES} multi_channel_common monitors)

if(NOT TARGET ie_samples)
    add_custom_target(ie_samples ALL)
endif()

if(COMMAND add_cpplint_target)
    add_cpplint_target(${TARGET_NAME}_cpplint FOR_TARGETS ${TARGET_NAME})
endif()

add_dependencies(ie_samples ${TARGET_NAME})
