

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHeaderView, QLabel,
    QSizePolicy, QTableView, QWidget)

class Ui_ResultsWindow(object):
    def setupUi(self, ResultsWindow):
        if not ResultsWindow.objectName():
            ResultsWindow.setObjectName(u"ResultsWindow")
        ResultsWindow.resize(935, 688)
        self.tableView = QTableView(ResultsWindow)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(40, 180, 871, 451))
        self.tableView.setAutoFillBackground(False)
        self.label = QLabel(ResultsWindow)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(400, 60, 181, 81))

        self.retranslateUi(ResultsWindow)

        QMetaObject.connectSlotsByName(ResultsWindow)
    # setupUi

    def retranslateUi(self, ResultsWindow):
        ResultsWindow.setWindowTitle(QCoreApplication.translate("ResultsWindow", u"results", None))
        self.label.setText(QCoreApplication.translate("ResultsWindow", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442", None))
    # retranslateUi

