//
// Created by Dmitri on 2026-10-17.
//

#include "CameraBridge.h"

CameraBridge::CameraBridge(QObject* parent) : QObject(parent) {}

void CameraBridge::OpenCamera(const QString &url) {
    emit CameraRequested(url);
}