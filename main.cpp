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
    window.show();

    return app.exec();
}
