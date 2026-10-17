
cmake_minimum_required(VERSION 4.3)
project(caltrans_highway_viewer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS
        Widgets
        WebEngineWidgets
        Multimedia
        MultimediaWidgets
        WebChannel
)

add_executable(caltrans_highway_viewer
        main.cpp
        ui/CameraWindow.cpp
        ui/CameraWindow.h
        ui/MainWindow.cpp
        ui/MainWindow.h
        ui/CameraBridge.cpp
        ui/CameraBridge.h
)

target_link_libraries(caltrans_highway_viewer PRIVATE
        Qt6::Widgets
        Qt6::WebEngineWidgets
        Qt6::Multimedia
        Qt6::MultimediaWidgets
        Qt6::WebChannel
)
