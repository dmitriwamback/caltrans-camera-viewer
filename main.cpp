#include <iostream>

#include <QApplication>
#include <QMainWindow>
#include <QWebEngineView>
#include <QUrl>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    QMainWindow window;

    auto *map = new QWebEngineView(&window);

    // IMPLEMENT QMULTIMEDIA FOR THIS
    //map->load(QUrl("https://wzmedia.dot.ca.gov/D3/5_Seamas_Ave_JNO_SAC5_SB.stream/playlist.m3u"));
    map->load(QUrl("http://127.0.0.1:8080/"));

    window.setCentralWidget(map);
    window.resize(1200, 800);
    window.setWindowTitle("Camera");
    window.show();

    return app.exec();
}