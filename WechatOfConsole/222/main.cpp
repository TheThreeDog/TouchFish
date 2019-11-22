#include "mainwindow.h"
#include <QApplication>
#include <QTranslator>

int main(int argc, char *argv[])
{
	QApplication app(argc, argv);

	QString translatorFileName = "/home/threedog/222/222_zh_CN.qm";
	QTranslator *translator = new QTranslator(&app);
	if (translator->load(translatorFileName))
		app.installTranslator(translator);

	MainWindow w; //加载过翻译文件再生成窗体才有翻译效果
	w.show();

	return app.exec();
}
