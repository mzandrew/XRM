
#----------------------------------------------------------------------------
# Setup the project
cmake_minimum_required(VERSION 2.6 FATAL_ERROR)
project(XRM)

#----------------------------------------------------------------------------
# Find Geant4 package, activating all available UI and Vis drivers by default
# You can set WITH_GEANT4_UIVIS to OFF via the command line or ccmake/cmake-gui
# to build a batch mode only executable
#
option(WITH_GEANT4_UIVIS "Build example with Geant4 UI and Vis drivers" ON)
if(WITH_GEANT4_UIVIS)
  find_package(Geant4 REQUIRED ui_all vis_all)
else()
  find_package(Geant4 REQUIRED)
endif()

#----------------------------------------------------------------------------
# Setup Geant4 include directories and compile definitions
# Setup include directory for this project
#
include(${Geant4_USE_FILE})
include_directories(${PROJECT_SOURCE_DIR}/include)


#----------------------------------------------------------------------------
# Locate sources and headers for this project
# NB: headers are included so they will show up in IDEs
#
file(GLOB sources ${PROJECT_SOURCE_DIR}/src/*.cc)
file(GLOB headers ${PROJECT_SOURCE_DIR}/include/*.hh)

#----------------------------------------------------------------------------
# Add the executable, and link it to the Geant4 libraries
#
#add_executable(exampleB1 exampleB1.cc ${sources} ${headers})
#target_link_libraries(exampleB1 ${Geant4_LIBRARIES})

add_executable(bulk_si_HER exampleB1.cc ${sources} ${headers})
target_link_libraries(bulk_si_HER ${Geant4_LIBRARIES})
target_compile_definitions(bulk_si_HER PRIVATE HER=1 BULK_SI_SITUATION=1)

add_executable(edge_on_HER exampleB1.cc ${sources} ${headers})
target_link_libraries(edge_on_HER ${Geant4_LIBRARIES})
target_compile_definitions(edge_on_HER PRIVATE HER=1 EDGE_ON=1)

add_executable(edge_on_scint_HER exampleB1.cc ${sources} ${headers})
target_link_libraries(edge_on_scint_HER ${Geant4_LIBRARIES})
target_compile_definitions(edge_on_scint_HER PRIVATE HER=1 EDGE_ON=1 SCINTILLATOR_PRESENT=1)

add_executable(edge_on_scint_gold_HER exampleB1.cc ${sources} ${headers})
target_link_libraries(edge_on_scint_gold_HER ${Geant4_LIBRARIES})
target_compile_definitions(edge_on_scint_gold_HER PRIVATE HER=1 EDGE_ON=1 SCINTILLATOR_PRESENT=1 MASK_FULL=1)

#add_executable(face_on_HER exampleB1.cc ${sources} ${headers})
#target_link_libraries(face_on_HER ${Geant4_LIBRARIES})
#target_compile_definitions(face_on_HER PRIVATE HER=1 FACE_ON=1)

add_executable(bulk_si_LER exampleB1.cc ${sources} ${headers})
target_link_libraries(bulk_si_LER ${Geant4_LIBRARIES})
target_compile_definitions(bulk_si_LER PRIVATE LER=1 BULK_SI_SITUATION=1)

add_executable(edge_on_LER exampleB1.cc ${sources} ${headers})
target_link_libraries(edge_on_LER ${Geant4_LIBRARIES})
target_compile_definitions(edge_on_LER PRIVATE LER=1 EDGE_ON=1)

add_executable(edge_on_scint_LER exampleB1.cc ${sources} ${headers})
target_link_libraries(edge_on_scint_LER ${Geant4_LIBRARIES})
target_compile_definitions(edge_on_scint_LER PRIVATE LER=1 EDGE_ON=1 SCINTILLATOR_PRESENT=1)

add_executable(edge_on_scint_gold_LER exampleB1.cc ${sources} ${headers})
target_link_libraries(edge_on_scint_gold_LER ${Geant4_LIBRARIES})
target_compile_definitions(edge_on_scint_gold_LER PRIVATE LER=1 EDGE_ON=1 SCINTILLATOR_PRESENT=1 MASK_FULL=1)

#add_executable(face_on_LER exampleB1.cc ${sources} ${headers})
#target_link_libraries(face_on_LER ${Geant4_LIBRARIES})
#target_compile_definitions(face_on_LER PRIVATE LER=1 FACE_ON=1)

#----------------------------------------------------------------------------
# Copy all scripts to the build directory, i.e. the directory in which we
# build B1. This is so that we can run the executable directly because it
# relies on these scripts being in the current working directory.
#
set(EXAMPLEB1_SCRIPTS
  exampleB1.in
  exampleB1.out
  init_vis.mac
  run1.mac
  run2.mac
  vis.mac
  HER-1-bunch.mac
  HER-N-bunches.mac
  LER-1-bunch.mac
  LER-N-bunches.mac
  )

foreach(_script ${EXAMPLEB1_SCRIPTS})
  configure_file(
    ${PROJECT_SOURCE_DIR}/${_script}
    ${PROJECT_BINARY_DIR}/${_script}
    COPYONLY
    )
endforeach()

#----------------------------------------------------------------------------
# For internal Geant4 use - but has no effect if you build this
# example standalone
#
add_custom_target(XRM DEPENDS edge_on_HER)

#----------------------------------------------------------------------------
# Install the executable to 'bin' directory under CMAKE_INSTALL_PREFIX
#
install(TARGETS bulk_si_HER DESTINATION bin)
install(TARGETS edge_on_HER DESTINATION bin)
install(TARGETS edge_on_scint_HER DESTINATION bin)
install(TARGETS edge_on_scint_gold_HER DESTINATION bin)
#install(TARGETS face_on_HER DESTINATION bin)
install(TARGETS bulk_si_LER DESTINATION bin)
install(TARGETS edge_on_LER DESTINATION bin)
install(TARGETS edge_on_scint_LER DESTINATION bin)
install(TARGETS edge_on_scint_gold_LER DESTINATION bin)
#install(TARGETS face_on_LER DESTINATION bin)

