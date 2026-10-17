cmake_minimum_required(VERSION 4.3)
project(caltrans_highway_viewer)

set(CMAKE_CXX_STANDARD 20)

find_package(Qt6 REQUIRED COMPONENTS
        Widgets
        WebEngineWidgets
        Multimedia
        MultimediaWidgets
)

add_executable(caltrans_highway_viewer main.cpp
        ui/CameraWindow.cpp
        ui/CameraWindow.h
        ui/MainWindow.cpp
        ui/MainWindow.h)

target_link_libraries(caltrans_highway_viewer PRIVATE
        Qt6::Widgets
        Qt6::WebEngineWidgets
        Qt6::Multimedia
        Qt6::MultimediaWidgets
)
