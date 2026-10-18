//
// Created by Dmitri on 2026-10-17.
//

#include "MainWindow.h"

#include "CameraWindow.h"

#include <QWebChannel>
#include <QWebEngineView>
#include <QUrl>
#include <QApplication>
#include <QCloseEvent>

MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent) {

    mapView = new QWebEngineView(this);
    channel = new QWebChannel(this);
    bridge = new CameraBridge(this);

    channel->registerObject("bridge", bridge);
    mapView->page()->setWebChannel(channel);

    connect(bridge, &CameraBridge::CameraRequested, this, &MainWindow::OpenCameraWindow);
    mapView->load(QUrl("http://127.0.0.1:8080/"));

    setCentralWidget(mapView);
    resize(1200, 800);
    setWindowTitle("Caltrans Camera Map");
}

void MainWindow::OpenCameraWindow(const QString& url, const QString& title) {
    auto* camera = new CameraWindow(url);
    camera->setAttribute(Qt::WA_DeleteOnClose);
    camera->setWindowTitle(title);
    camera->show();
}

void MainWindow::closeEvent(QCloseEvent* event) {
    event->accept();
    QApplication::quit();
}
