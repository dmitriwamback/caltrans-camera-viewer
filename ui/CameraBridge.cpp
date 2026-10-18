//
// Created by Dmitri on 2026-10-17.
//

#include "CameraBridge.h"

#include <iostream>

CameraBridge::CameraBridge(QObject* parent) : QObject(parent) {}

void CameraBridge::OpenCamera(const QString &url, const QString& name) {
    emit CameraRequested(url, name);
}