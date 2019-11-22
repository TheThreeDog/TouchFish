#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QApplication>
#include <QTranslator>
#include <QLabel>

MainWindow::MainWindow(QWidget *parent) :
	QMainWindow(parent),
	ui(new Ui::MainWindow)
{
	ui->setupUi(this);
	tr("Test Text");
	m_pLabel = new QLabel(tr("Test Text"),this);
	m_pLabel->move(200,200);

}

MainWindow::~MainWindow()
{
	delete ui;
}
