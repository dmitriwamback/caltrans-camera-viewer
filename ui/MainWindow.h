//
// Created by Dmitri on 2026-10-17.
//

#ifndef CALTRANS_HIGHWAY_VIEWER_MAINWINDOW_H
#define CALTRANS_HIGHWAY_VIEWER_MAINWINDOW_H


#include <QMainWindow>
#include <QCloseEvent>
#include <QApplication>

class MainWindow : public QMainWindow {
public:
    explicit MainWindow(QWidget* parent = nullptr);

protected:
    void closeEvent(QCloseEvent* event) override;
};

#endif //CALTRANS_HIGHWAY_VIEWER_MAINWINDOW_H
