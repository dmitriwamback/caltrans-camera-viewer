//
// Created by Dmitri on 2026-10-17.
//

#include "CameraWindow.h"

#include <QMediaPlayer>
#include <QVideoWidget>
#include <QAudioOutput>
#include <QUrl>

CameraWindow::CameraWindow(const QString& url, QWidget* parent) : QMainWindow(parent) {
    auto* video = new QVideoWidget(this);
    auto* player = new QMediaPlayer(this);
    auto* audio = new QAudioOutput(this);

    player->setVideoOutput(video);
    player->setAudioOutput(audio);
    player->setSource(QUrl(url));

    setCentralWidget(video);
    resize(800, 500);
    setWindowTitle("Camera");
    player->play();
}