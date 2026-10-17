#include <iostream>

#include <QApplication>
#include <QMainWindow>
#include <QWebEngineView>
#include <QUrl>

#include "ui/CameraWindow.h"
#include "ui/MainWindow.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    MainWindow window;

    auto *map = new QWebEngineView(&window);
    map->load(QUrl("http://127.0.0.1:8080/"));

    window.setCentralWidget(map);
    window.resize(1200, 800);
    window.setWindowTitle("Map");
    window.show();

    auto* camera1 = new CameraWindow("https://wzmedia.dot.ca.gov/D3/5_Seamas_Ave_JNO_SAC5_SB.stream/playlist.m3u");
    camera1->show();

    return app.exec();
}
