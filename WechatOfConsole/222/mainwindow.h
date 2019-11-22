#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
class QLabel;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
	Q_OBJECT

public:
	explicit MainWindow(QWidget *parent = nullptr);
	void retranslate();
	~MainWindow();

private slots:
	void on_action_triggered();

	void on_actionEnglish_triggered();

private:
	Ui::MainWindow *ui;
	QLabel * m_pLabel;
};

#endif // MAINWINDOW_H
