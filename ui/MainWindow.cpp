//
// Created by Dmitri on 2026-10-17.
//

#include "MainWindow.h"

MainWindow::MainWindow(QWidget* parent) : QMainWindow(parent) {}

void MainWindow::closeEvent(QCloseEvent* event) {
    event->accept();
    QApplication::quit();
}
