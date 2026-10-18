//
// Created by Dmitri on 2026-10-17.
//

#ifndef CALTRANS_HIGHWAY_VIEWER_CAMERABRIDGE_H
#define CALTRANS_HIGHWAY_VIEWER_CAMERABRIDGE_H

#include <QObject>
#include <QString>

class CameraBridge: public QObject {
    Q_OBJECT

public:
    explicit CameraBridge(QObject* parent = nullptr);

public slots:
    void OpenCamera(const QString& url, const QString& name);

signals:
    void CameraRequested(const QString& url, const QString& name);
};


#endif //CALTRANS_HIGHWAY_VIEWER_CAMERABRIDGE_H
