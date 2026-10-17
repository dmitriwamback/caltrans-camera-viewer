//
// Created by Dmitri on 2026-10-17.
//

#ifndef CALTRANS_HIGHWAY_VIEWER_CAMERAWINDOW_H
#define CALTRANS_HIGHWAY_VIEWER_CAMERAWINDOW_H

#include <QMainWindow>

class CameraWindow: public QMainWindow {
public:
    explicit CameraWindow(const QString& url, QWidget* parent = nullptr);
};


#endif //CALTRANS_HIGHWAY_VIEWER_CAMERAWINDOW_H
