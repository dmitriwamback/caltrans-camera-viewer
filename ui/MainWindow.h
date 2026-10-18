//
// Created by Dmitri on 2026-10-17.
//

#ifndef CALTRANS_HIGHWAY_VIEWER_MAINWINDOW_H
#define CALTRANS_HIGHWAY_VIEWER_MAINWINDOW_H


#include <QMainWindow>
#include <QCloseEvent>
#include <QApplication>
#include <QWebEngineView>

#include "CameraBridge.h"

class MainWindow : public QMainWindow {
public:
    explicit MainWindow(QWidget* parent = nullptr);

private slots:
    void OpenCameraWindow(const QString& url, const QString& title);

protected:
    void closeEvent(QCloseEvent* event) override;

private:
    QWebEngineView* mapView;
    QWebChannel* channel;
    CameraBridge* bridge;
};

#endif //CALTRANS_HIGHWAY_VIEWER_MAINWINDOW_H
