# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QStackedWidget, QTableView, QTextEdit, QTimeEdit,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1268, 720)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(33, 37, 43, 180);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background"
                        "-color: rgb(40, 44, 52);\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#topLogo {\n"
"	background-color: rgb(33, 37, 43);\n"
"	background-image: url(:/images/images/images/PyDracula.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; }\n"
"#titleLeftDescription { font: 8pt \"Segoe UI\"; color: rgb(189, 147, 249); }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: rgb(18"
                        "9, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: rgb(37, 41, 48);\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(113, 126, 149);\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: rgb("
                        "189, 147, 249);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: rgb(44, 49, 58);\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border"
                        "-top: 3px solid rgb(40, 44, 52);\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid rgb(44, 49, 58);\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: rgb(44, 49, 57); border-sty"
                        "le: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: rgb(44, 49, 58); }\n"
"#themeSettingsTopDetail { background-color: rgb(189, 147, 249); }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: rgb(44, 49, 58); }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(113, 126, 149); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: rgb(40, 44, 52);\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb"
                        "(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: rgb(44, 49, 58);\n"
"	border-bottom: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: rgb(44, 49, 60);\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: rgb(33, 37, 43);\n"
"	max-width: 30px;\n"
"	border: 1px solid rgb(44, 49, 58);\n"
"	border-style: none;\n"
"    border-bottom: 1px solid rgb(44, 49, 60);\n"
"    border-right: 1px solid rgb(44, 49, 60);\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: rgb(33, 37, 43);\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid rgb(33, 37, 43);\n"
"	background-co"
                        "lor: rgb(33, 37, 43);\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid rgb(44, 49, 60);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: rgb(33, 37, 43);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-c"
                        "olor: rgb(255, 121, 198);\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
""
                        "QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     su"
                        "bcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"	back"
                        "ground-image: url(:/icons/images/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"	border: 3px solid rgb(52, 59, 72);	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: rgb(27, 29, 35);\n"
"	border-radius: 5px;\n"
"	border: 2px solid rgb(33, 37, 43);\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subco"
                        "ntrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: rgba(39, 44, 54, 150);\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/images/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: rgb(33, 37, 43);\n"
"	padding: 10px;\n"
"	selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    h"
                        "eight: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"QCommandLi"
                        "nkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"	color: rgb(255, 170, 255);\n"
"}\n"
"QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: rgb(44, 49, 60);\n"
"}\n"
"QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: rgb(52, 58, 71);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid rgb(52, 59, 72);\n"
"	border-radius: 5px;	\n"
"	background-color: rgb(52, 59, 72);\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: rgb(57, 65, 80);\n"
"	border: 2px solid rgb(61, 70, 86);\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: rgb(35, 40, 49);\n"
"	border: 2px solid rgb(43, 50, 61);\n"
"}\n"
"\n"
"")
        self.appMargins = QVBoxLayout(self.styleSheet)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI Semibold"])
        font1.setPointSize(12)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftApp.setFont(font1)
        self.titleLeftApp.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(8)
        font2.setBold(False)
        font2.setItalic(False)
        self.titleLeftDescription.setFont(font2)
        self.titleLeftDescription.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setEnabled(True)
        self.leftMenuFrame.setMaximumSize(QSize(60, 648))
        self.leftMenuFrame.setFrameShape(QFrame.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Raised)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setGeometry(QRect(0, 3, 60, 45))
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setGeometry(QRect(0, 48, 60, 243))
        self.topMenu.setFrameShape(QFrame.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_widgets = QPushButton(self.topMenu)
        self.btn_widgets.setObjectName(u"btn_widgets")
        sizePolicy.setHeightForWidth(self.btn_widgets.sizePolicy().hasHeightForWidth())
        self.btn_widgets.setSizePolicy(sizePolicy)
        self.btn_widgets.setMinimumSize(QSize(0, 45))
        self.btn_widgets.setFont(font)
        self.btn_widgets.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_widgets.setLayoutDirection(Qt.LeftToRight)
        self.btn_widgets.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-gamepad.png);")

        self.verticalLayout_8.addWidget(self.btn_widgets)

        self.btn_new = QPushButton(self.topMenu)
        self.btn_new.setObjectName(u"btn_new")
        sizePolicy.setHeightForWidth(self.btn_new.sizePolicy().hasHeightForWidth())
        self.btn_new.setSizePolicy(sizePolicy)
        self.btn_new.setMinimumSize(QSize(0, 45))
        self.btn_new.setFont(font)
        self.btn_new.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_new.setLayoutDirection(Qt.LeftToRight)
        self.btn_new.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-file.png);")

        self.verticalLayout_8.addWidget(self.btn_new)

        self.btn_save = QPushButton(self.topMenu)
        self.btn_save.setObjectName(u"btn_save")
        sizePolicy.setHeightForWidth(self.btn_save.sizePolicy().hasHeightForWidth())
        self.btn_save.setSizePolicy(sizePolicy)
        self.btn_save.setMinimumSize(QSize(0, 45))
        self.btn_save.setFont(font)
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.setLayoutDirection(Qt.LeftToRight)
        self.btn_save.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-data-transfer-up.png);")

        self.verticalLayout_8.addWidget(self.btn_save)

        self.btn_exit = QPushButton(self.topMenu)
        self.btn_exit.setObjectName(u"btn_exit")
        sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        self.btn_exit.setSizePolicy(sizePolicy)
        self.btn_exit.setMinimumSize(QSize(0, 45))
        self.btn_exit.setFont(font)
        self.btn_exit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_exit.setLayoutDirection(Qt.LeftToRight)
        self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x.png);")

        self.verticalLayout_8.addWidget(self.btn_exit)

        self.deposit_btn = QPushButton(self.topMenu)
        self.deposit_btn.setObjectName(u"deposit_btn")
        self.deposit_btn.setMinimumSize(QSize(0, 18))
        self.deposit_btn.setMaximumSize(QSize(60, 18))
        self.deposit_btn.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-data-transfer-down.png);\n"
"QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	margin: 30px;\n"
"	padding-top: 45px;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/cil-data-transfer-down.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.deposit_btn.setIcon(icon)

        self.verticalLayout_8.addWidget(self.deposit_btn)

        self.register_in_ts_btn = QPushButton(self.topMenu)
        self.register_in_ts_btn.setObjectName(u"register_in_ts_btn")
        self.register_in_ts_btn.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-mouse.png);")

        self.verticalLayout_8.addWidget(self.register_in_ts_btn)

        self.volume_btn = QPushButton(self.topMenu)
        self.volume_btn.setObjectName(u"volume_btn")
        self.volume_btn.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-paint-bucket.png);")

        self.verticalLayout_8.addWidget(self.volume_btn)

        self.exact_coin_menu = QPushButton(self.topMenu)
        self.exact_coin_menu.setObjectName(u"exact_coin_menu")
        self.exact_coin_menu.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-find-in-page.png);")

        self.verticalLayout_8.addWidget(self.exact_coin_menu)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setGeometry(QRect(0, 603, 60, 45))
        self.bottomMenu.setFrameShape(QFrame.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.toggleLeftBox = QPushButton(self.bottomMenu)
        self.toggleLeftBox.setObjectName(u"toggleLeftBox")
        sizePolicy.setHeightForWidth(self.toggleLeftBox.sizePolicy().hasHeightForWidth())
        self.toggleLeftBox.setSizePolicy(sizePolicy)
        self.toggleLeftBox.setMinimumSize(QSize(0, 45))
        self.toggleLeftBox.setFont(font)
        self.toggleLeftBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleLeftBox.setLayoutDirection(Qt.LeftToRight)
        self.toggleLeftBox.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_settings.png);")

        self.verticalLayout_9.addWidget(self.toggleLeftBox)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraIcon = QFrame(self.extraTopBg)
        self.extraIcon.setObjectName(u"extraIcon")
        self.extraIcon.setMinimumSize(QSize(20, 0))
        self.extraIcon.setMaximumSize(QSize(20, 20))
        self.extraIcon.setFrameShape(QFrame.NoFrame)
        self.extraIcon.setFrameShadow(QFrame.Raised)

        self.extraTopLayout.addWidget(self.extraIcon, 0, 0, 1, 1)

        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.extraCloseColumnBtn.setIcon(icon1)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_share = QPushButton(self.extraTopMenu)
        self.btn_share.setObjectName(u"btn_share")
        sizePolicy.setHeightForWidth(self.btn_share.sizePolicy().hasHeightForWidth())
        self.btn_share.setSizePolicy(sizePolicy)
        self.btn_share.setMinimumSize(QSize(0, 45))
        self.btn_share.setFont(font)
        self.btn_share.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_share.setLayoutDirection(Qt.LeftToRight)
        self.btn_share.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-share-boxed.png);")

        self.verticalLayout_11.addWidget(self.btn_share)

        self.btn_adjustments = QPushButton(self.extraTopMenu)
        self.btn_adjustments.setObjectName(u"btn_adjustments")
        sizePolicy.setHeightForWidth(self.btn_adjustments.sizePolicy().hasHeightForWidth())
        self.btn_adjustments.setSizePolicy(sizePolicy)
        self.btn_adjustments.setMinimumSize(QSize(0, 45))
        self.btn_adjustments.setFont(font)
        self.btn_adjustments.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_adjustments.setLayoutDirection(Qt.LeftToRight)
        self.btn_adjustments.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-equalizer.png);")

        self.verticalLayout_11.addWidget(self.btn_adjustments)

        self.btn_more = QPushButton(self.extraTopMenu)
        self.btn_more.setObjectName(u"btn_more")
        sizePolicy.setHeightForWidth(self.btn_more.sizePolicy().hasHeightForWidth())
        self.btn_more.setSizePolicy(sizePolicy)
        self.btn_more.setMinimumSize(QSize(0, 45))
        self.btn_more.setFont(font)
        self.btn_more.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_more.setLayoutDirection(Qt.LeftToRight)
        self.btn_more.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-layers.png);")

        self.verticalLayout_11.addWidget(self.btn_more)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.textEdit = QTextEdit(self.extraCenter)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setMinimumSize(QSize(222, 0))
        self.textEdit.setStyleSheet(u"background: transparent;")
        self.textEdit.setFrameShape(QFrame.NoFrame)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.textEdit)


        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.settingsTopBtn = QPushButton(self.rightButtons)
        self.settingsTopBtn.setObjectName(u"settingsTopBtn")
        self.settingsTopBtn.setMinimumSize(QSize(28, 28))
        self.settingsTopBtn.setMaximumSize(QSize(28, 28))
        self.settingsTopBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settingsTopBtn.setIcon(icon2)
        self.settingsTopBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.settingsTopBtn)

        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeAppBtn.setIcon(icon3)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font3)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon4 = QIcon()
        icon4.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeRestoreAppBtn.setIcon(icon4)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.closeAppBtn.setIcon(icon1)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.NoFrame)
        self.content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.add_accs_button = QPushButton(self.home)
        self.add_accs_button.setObjectName(u"add_accs_button")
        self.add_accs_button.setGeometry(QRect(20, 50, 121, 51))
        self.register_btn = QPushButton(self.home)
        self.register_btn.setObjectName(u"register_btn")
        self.register_btn.setGeometry(QRect(350, 40, 161, 51))
        self.delete_btn = QPushButton(self.home)
        self.delete_btn.setObjectName(u"delete_btn")
        self.delete_btn.setGeometry(QRect(760, 50, 141, 61))
        self.tableView = QTableView(self.home)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setGeometry(QRect(60, 130, 911, 371))
        self.tableView.setAutoFillBackground(False)
        self.result_btn = QPushButton(self.home)
        self.result_btn.setObjectName(u"result_btn")
        self.result_btn.setGeometry(QRect(360, 530, 191, 61))
        self.main_timeEdit = QTimeEdit(self.home)
        self.main_timeEdit.setObjectName(u"main_timeEdit")
        self.main_timeEdit.setGeometry(QRect(990, 250, 121, 41))
        self.label_6 = QLabel(self.home)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(980, 180, 161, 41))
        self.affilate_id_input = QLineEdit(self.home)
        self.affilate_id_input.setObjectName(u"affilate_id_input")
        self.affilate_id_input.setGeometry(QRect(540, 30, 113, 20))
        self.group_id_input = QLineEdit(self.home)
        self.group_id_input.setObjectName(u"group_id_input")
        self.group_id_input.setGeometry(QRect(540, 60, 111, 21))
        self.group_type_edit = QLineEdit(self.home)
        self.group_type_edit.setObjectName(u"group_type_edit")
        self.group_type_edit.setGeometry(QRect(540, 90, 111, 21))
        self.excel_start_edit = QLineEdit(self.home)
        self.excel_start_edit.setObjectName(u"excel_start_edit")
        self.excel_start_edit.setGeometry(QRect(160, 50, 113, 20))
        self.excel_finish_edit = QLineEdit(self.home)
        self.excel_finish_edit.setObjectName(u"excel_finish_edit")
        self.excel_finish_edit.setGeometry(QRect(160, 80, 113, 20))
        self.stackedWidget.addWidget(self.home)
        self.exact_coin_balance = QWidget()
        self.exact_coin_balance.setObjectName(u"exact_coin_balance")
        self.coin_balance_tableView = QTableView(self.exact_coin_balance)
        self.coin_balance_tableView.setObjectName(u"coin_balance_tableView")
        self.coin_balance_tableView.setGeometry(QRect(20, 80, 971, 511))
        self.label_13 = QLabel(self.exact_coin_balance)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(100, 20, 181, 41))
        self.exact_coin_lineEdit = QLineEdit(self.exact_coin_balance)
        self.exact_coin_lineEdit.setObjectName(u"exact_coin_lineEdit")
        self.exact_coin_lineEdit.setGeometry(QRect(1000, 80, 131, 21))
        self.exact_coin_pushButton = QPushButton(self.exact_coin_balance)
        self.exact_coin_pushButton.setObjectName(u"exact_coin_pushButton")
        self.exact_coin_pushButton.setGeometry(QRect(1010, 150, 121, 91))
        self.stackedWidget.addWidget(self.exact_coin_balance)
        self.widgets = QWidget()
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"b")
        self.tableView_set_up = QTableView(self.widgets)
        self.tableView_set_up.setObjectName(u"tableView_set_up")
        self.tableView_set_up.setGeometry(QRect(20, 110, 631, 451))
        self.tableView_set_up.setAutoFillBackground(True)
        self.label_2 = QLabel(self.widgets)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(280, 30, 301, 61))
        self.fa2_checkbox = QCheckBox(self.widgets)
        self.fa2_checkbox.setObjectName(u"fa2_checkbox")
        self.fa2_checkbox.setGeometry(QRect(690, 120, 81, 51))
        self.wl_on_checkbox = QCheckBox(self.widgets)
        self.wl_on_checkbox.setObjectName(u"wl_on_checkbox")
        self.wl_on_checkbox.setGeometry(QRect(690, 180, 141, 61))
        self.add_wallet_checkbox = QCheckBox(self.widgets)
        self.add_wallet_checkbox.setObjectName(u"add_wallet_checkbox")
        self.add_wallet_checkbox.setGeometry(QRect(690, 230, 321, 71))
        self.only_wl_checkbox = QCheckBox(self.widgets)
        self.only_wl_checkbox.setObjectName(u"only_wl_checkbox")
        self.only_wl_checkbox.setGeometry(QRect(690, 290, 181, 61))
        self.block_checkbox = QCheckBox(self.widgets)
        self.block_checkbox.setObjectName(u"block_checkbox")
        self.block_checkbox.setGeometry(QRect(690, 350, 301, 61))
        self.set_up_button = QPushButton(self.widgets)
        self.set_up_button.setObjectName(u"set_up_button")
        self.set_up_button.setGeometry(QRect(700, 440, 131, 121))
        self.label_7 = QLabel(self.widgets)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(950, 400, 151, 61))
        self.set_up_timeEdit = QTimeEdit(self.widgets)
        self.set_up_timeEdit.setObjectName(u"set_up_timeEdit")
        self.set_up_timeEdit.setGeometry(QRect(950, 510, 118, 22))
        self.change_password_checkbox = QCheckBox(self.widgets)
        self.change_password_checkbox.setObjectName(u"change_password_checkbox")
        self.change_password_checkbox.setGeometry(QRect(690, 90, 151, 21))
        self.stackedWidget.addWidget(self.widgets)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.collect_window = QListView(self.page)
        self.collect_window.setObjectName(u"collect_window")
        self.collect_window.setGeometry(QRect(30, 30, 621, 551))
        self.pushButton = QPushButton(self.page)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(820, 470, 151, 91))
        self.withdraw_address_input = QLineEdit(self.page)
        self.withdraw_address_input.setObjectName(u"withdraw_address_input")
        self.withdraw_address_input.setGeometry(QRect(830, 70, 151, 31))
        self.stackedWidget.addWidget(self.page)
        self.new_page = QWidget()
        self.new_page.setObjectName(u"new_page")
        self.launch_profile_table_view = QTableView(self.new_page)
        self.launch_profile_table_view.setObjectName(u"launch_profile_table_view")
        self.launch_profile_table_view.setGeometry(QRect(40, 100, 701, 491))
        self.launch_profile_btn = QPushButton(self.new_page)
        self.launch_profile_btn.setObjectName(u"launch_profile_btn")
        self.launch_profile_btn.setGeometry(QRect(860, 250, 121, 111))
        self.label = QLabel(self.new_page)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(350, 30, 441, 51))
        self.stackedWidget.addWidget(self.new_page)
        self.withdraw = QWidget()
        self.withdraw.setObjectName(u"withdraw")
        self.withdraw_tableView = QTableView(self.withdraw)
        self.withdraw_tableView.setObjectName(u"withdraw_tableView")
        self.withdraw_tableView.setGeometry(QRect(10, 120, 601, 461))
        self.label_3 = QLabel(self.withdraw)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(240, 30, 101, 71))
        self.label_4 = QLabel(self.withdraw)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(670, 20, 101, 71))
        self.radioButton = QRadioButton(self.withdraw)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(680, 120, 83, 18))
        self.radioButton_2 = QRadioButton(self.withdraw)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(680, 180, 83, 18))
        self.radioButton_3 = QRadioButton(self.withdraw)
        self.radioButton_3.setObjectName(u"radioButton_3")
        self.radioButton_3.setGeometry(QRect(680, 250, 83, 18))
        self.launch_withdraw_btn = QPushButton(self.withdraw)
        self.launch_withdraw_btn.setObjectName(u"launch_withdraw_btn")
        self.launch_withdraw_btn.setGeometry(QRect(680, 430, 161, 131))
        self.withdraw_timeEdit = QTimeEdit(self.withdraw)
        self.withdraw_timeEdit.setObjectName(u"withdraw_timeEdit")
        self.withdraw_timeEdit.setGeometry(QRect(680, 360, 118, 22))
        self.label_5 = QLabel(self.withdraw)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(680, 303, 261, 51))
        self.stackedWidget.addWidget(self.withdraw)
        self.data = QWidget()
        self.data.setObjectName(u"data")
        self.data_tableView = QTableView(self.data)
        self.data_tableView.setObjectName(u"data_tableView")
        self.data_tableView.setGeometry(QRect(30, 20, 871, 571))
        self.listView = QListView(self.data)
        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(930, 110, 221, 171))
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.data_btn = QPushButton(self.data)
        self.data_btn.setObjectName(u"data_btn")
        self.data_btn.setGeometry(QRect(940, 410, 181, 131))
        self.label_8 = QLabel(self.data)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(930, 20, 191, 71))
        self.data_time = QTimeEdit(self.data)
        self.data_time.setObjectName(u"data_time")
        self.data_time.setGeometry(QRect(930, 330, 118, 22))
        self.stackedWidget.addWidget(self.data)
        self.deposit = QWidget()
        self.deposit.setObjectName(u"deposit")
        self.chain_name_edit = QLineEdit(self.deposit)
        self.chain_name_edit.setObjectName(u"chain_name_edit")
        self.chain_name_edit.setGeometry(QRect(830, 90, 181, 31))
        self.coin_edit = QLineEdit(self.deposit)
        self.coin_edit.setObjectName(u"coin_edit")
        self.coin_edit.setGeometry(QRect(830, 130, 181, 31))
        self.deposit_tableView = QTableView(self.deposit)
        self.deposit_tableView.setObjectName(u"deposit_tableView")
        self.deposit_tableView.setGeometry(QRect(30, 90, 791, 501))
        self.label_9 = QLabel(self.deposit)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(30, 20, 151, 51))
        self.min_amount_edit = QLineEdit(self.deposit)
        self.min_amount_edit.setObjectName(u"min_amount_edit")
        self.min_amount_edit.setGeometry(QRect(830, 170, 181, 31))
        self.random_range_edit_start = QLineEdit(self.deposit)
        self.random_range_edit_start.setObjectName(u"random_range_edit_start")
        self.random_range_edit_start.setGeometry(QRect(830, 270, 121, 31))
        self.deposit_btn_launch = QPushButton(self.deposit)
        self.deposit_btn_launch.setObjectName(u"deposit_btn_launch")
        self.deposit_btn_launch.setGeometry(QRect(840, 480, 191, 101))
        self.radioButton_4 = QRadioButton(self.deposit)
        self.radioButton_4.setObjectName(u"radioButton_4")
        self.radioButton_4.setGeometry(QRect(670, 50, 91, 21))
        self.radioButton_4.setChecked(True)
        self.random_range_edit_finish = QLineEdit(self.deposit)
        self.random_range_edit_finish.setObjectName(u"random_range_edit_finish")
        self.random_range_edit_finish.setGeometry(QRect(970, 270, 131, 31))
        self.gas_coin_amount_edit = QLineEdit(self.deposit)
        self.gas_coin_amount_edit.setObjectName(u"gas_coin_amount_edit")
        self.gas_coin_amount_edit.setGeometry(QRect(830, 210, 181, 31))
        self.deposit_timer = QTimeEdit(self.deposit)
        self.deposit_timer.setObjectName(u"deposit_timer")
        self.deposit_timer.setGeometry(QRect(830, 330, 118, 22))
        self.deposit_networks_list = QListWidget(self.deposit)
        self.deposit_networks_list.setObjectName(u"deposit_networks_list")
        self.deposit_networks_list.setGeometry(QRect(1020, 90, 141, 151))
        self.stackedWidget.addWidget(self.deposit)
        self.volume = QWidget()
        self.volume.setObjectName(u"volume")
        self.volumeTableView = QTableView(self.volume)
        self.volumeTableView.setObjectName(u"volumeTableView")
        self.volumeTableView.setGeometry(QRect(10, 40, 991, 551))
        self.symbol_edit = QLineEdit(self.volume)
        self.symbol_edit.setObjectName(u"symbol_edit")
        self.symbol_edit.setGeometry(QRect(1020, 130, 111, 21))
        self.volume_edit = QLineEdit(self.volume)
        self.volume_edit.setObjectName(u"volume_edit")
        self.volume_edit.setGeometry(QRect(1020, 320, 113, 21))
        self.launch_volume_btn = QPushButton(self.volume)
        self.launch_volume_btn.setObjectName(u"launch_volume_btn")
        self.launch_volume_btn.setGeometry(QRect(1020, 490, 111, 61))
        self.label_11 = QLabel(self.volume)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(140, 10, 321, 21))
        self.volume_range_start = QLineEdit(self.volume)
        self.volume_range_start.setObjectName(u"volume_range_start")
        self.volume_range_start.setGeometry(QRect(1020, 390, 113, 20))
        self.volume_range_finish = QLineEdit(self.volume)
        self.volume_range_finish.setObjectName(u"volume_range_finish")
        self.volume_range_finish.setGeometry(QRect(1020, 420, 113, 20))
        self.label_12 = QLabel(self.volume)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(1020, 350, 121, 31))
        self.volume_timer = QTimeEdit(self.volume)
        self.volume_timer.setObjectName(u"volume_timer")
        self.volume_timer.setGeometry(QRect(1020, 460, 118, 22))
        self.VolumelistWidget = QListWidget(self.volume)
        self.VolumelistWidget.setObjectName(u"VolumelistWidget")
        self.VolumelistWidget.setGeometry(QRect(1020, 160, 121, 151))
        self.volume_checkBox = QCheckBox(self.volume)
        self.volume_checkBox.setObjectName(u"volume_checkBox")
        self.volume_checkBox.setGeometry(QRect(1020, 40, 131, 16))
        self.loan_checkBox = QCheckBox(self.volume)
        self.loan_checkBox.setObjectName(u"loan_checkBox")
        self.loan_checkBox.setGeometry(QRect(1020, 70, 131, 21))
        self.close_loan_chechbox = QCheckBox(self.volume)
        self.close_loan_chechbox.setObjectName(u"close_loan_chechbox")
        self.close_loan_chechbox.setGeometry(QRect(1020, 100, 141, 21))
        self.stackedWidget.addWidget(self.volume)
        self.tokensplash = QWidget()
        self.tokensplash.setObjectName(u"tokensplash")
        self.ts_edit = QLineEdit(self.tokensplash)
        self.ts_edit.setObjectName(u"ts_edit")
        self.ts_edit.setGeometry(QRect(1000, 100, 131, 31))
        self.ts_tableView = QTableView(self.tokensplash)
        self.ts_tableView.setObjectName(u"ts_tableView")
        self.ts_tableView.setGeometry(QRect(10, 90, 981, 511))
        self.register_in_st_btn = QPushButton(self.tokensplash)
        self.register_in_st_btn.setObjectName(u"register_in_st_btn")
        self.register_in_st_btn.setGeometry(QRect(1000, 170, 151, 111))
        self.label_10 = QLabel(self.tokensplash)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(220, 10, 141, 51))
        self.ts_timer = QTimeEdit(self.tokensplash)
        self.ts_timer.setObjectName(u"ts_timer")
        self.ts_timer.setGeometry(QRect(1010, 330, 118, 22))
        self.stackedWidget.addWidget(self.tokensplash)

        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.btn_message = QPushButton(self.topMenus)
        self.btn_message.setObjectName(u"btn_message")
        sizePolicy.setHeightForWidth(self.btn_message.sizePolicy().hasHeightForWidth())
        self.btn_message.setSizePolicy(sizePolicy)
        self.btn_message.setMinimumSize(QSize(0, 45))
        self.btn_message.setFont(font)
        self.btn_message.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_message.setLayoutDirection(Qt.LeftToRight)
        self.btn_message.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-envelope-open.png);")

        self.verticalLayout_14.addWidget(self.btn_message)

        self.btn_print = QPushButton(self.topMenus)
        self.btn_print.setObjectName(u"btn_print")
        sizePolicy.setHeightForWidth(self.btn_print.sizePolicy().hasHeightForWidth())
        self.btn_print.setSizePolicy(sizePolicy)
        self.btn_print.setMinimumSize(QSize(0, 45))
        self.btn_print.setFont(font)
        self.btn_print.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_print.setLayoutDirection(Qt.LeftToRight)
        self.btn_print.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-print.png);")

        self.verticalLayout_14.addWidget(self.btn_print)

        self.btn_logout = QPushButton(self.topMenus)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy)
        self.btn_logout.setMinimumSize(QSize(0, 45))
        self.btn_logout.setFont(font)
        self.btn_logout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_logout.setLayoutDirection(Qt.LeftToRight)
        self.btn_logout.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-account-logout.png);")

        self.verticalLayout_14.addWidget(self.btn_logout)


        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignTop)


        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setBold(False)
        font4.setItalic(False)
        self.creditsLabel.setFont(font4)
        self.creditsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.appMargins.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(8)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"PyDracula", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"Modern GUI / Flat Style", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_widgets.setText(QCoreApplication.translate("MainWindow", u"Widgets", None))
        self.btn_new.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.btn_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.deposit_btn.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.register_in_ts_btn.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.volume_btn.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.exact_coin_menu.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.toggleLeftBox.setText(QCoreApplication.translate("MainWindow", u"Left Box", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Left Box", None))
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.btn_share.setText(QCoreApplication.translate("MainWindow", u"Share", None))
        self.btn_adjustments.setText(QCoreApplication.translate("MainWindow", u"Adjustments", None))
        self.btn_more.setText(QCoreApplication.translate("MainWindow", u"More", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">PyDracula</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#ffffff;\">An interface created using Python and PySide (support for PyQt), and with colors based on the Dracula theme created by Zeno Rocha.</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><"
                        "span style=\" color:#ffffff;\">MIT License</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" color:#bd93f9;\">Created by: Wanderson M. Pimenta</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert UI</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\">pyside6-uic main.ui &gt; ui_main.py</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; color:#ff79c6;\">Convert QRC</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; "
                        "margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9pt; color:#ffffff;\">pyside6-rcc resources.qrc -o resources_rc.py</span></p></body></html>", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"Bybit Machine", None))
#if QT_CONFIG(tooltip)
        self.settingsTopBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Settings", None))
#endif // QT_CONFIG(tooltip)
        self.settingsTopBtn.setText("")
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.add_accs_button.setText(QCoreApplication.translate("MainWindow", u"\u0434\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u044b", None))
        self.register_btn.setText(QCoreApplication.translate("MainWindow", u"\u0437\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0430\u043a\u0438\u0438", None))
        self.delete_btn.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u044b", None))
        self.result_btn.setText(QCoreApplication.translate("MainWindow", u"\u041b\u043e\u0433\u0438\u043d", None))
        self.main_timeEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"mm:ss", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0434\u0435\u0440\u0436\u043a\u0430 \u043c\u0435\u0436\u0434\u0443 \u0430\u043a\u043a\u0430\u043c\u0438", None))
        self.affilate_id_input.setText(QCoreApplication.translate("MainWindow", u"affilate_id", None))
        self.group_id_input.setText(QCoreApplication.translate("MainWindow", u"group_id", None))
        self.group_type_edit.setText(QCoreApplication.translate("MainWindow", u"group_type", None))
        self.excel_start_edit.setText(QCoreApplication.translate("MainWindow", u"start", None))
        self.excel_finish_edit.setText(QCoreApplication.translate("MainWindow", u"finish", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u0411\u0430\u043b\u0430\u043d\u0441 \u043a\u043e\u043d\u043a\u0440\u0435\u0442\u043d\u043e\u0439 \u043c\u043e\u043d\u0435\u0442\u044b", None))
        self.exact_coin_lineEdit.setText(QCoreApplication.translate("MainWindow", u"\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043c\u043e\u043d\u0435\u0442\u044b", None))
        self.exact_coin_pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 \u0430\u043a\u043e\u0432", None))
        self.fa2_checkbox.setText(QCoreApplication.translate("MainWindow", u"add 2fa", None))
        self.wl_on_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u0412\u043a\u043b\u044e\u0447\u0438\u0442\u044c whitelist", None))
        self.add_wallet_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c web3 \u043a\u043e\u0448\u0435\u043b\u044c \u0438 \u0434\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0435\u0433\u043e \u0432 whitelist", None))
        self.only_wl_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0432\u043e\u0434 \u0422\u041e\u041b\u042c\u041a\u041e \u0447\u0435\u0440\u0435\u0437 wl", None))
        self.block_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0431\u0440\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u0435 \u043d\u0432\u043e\u044b\u0445 \u0430\u0434\u0440\u0435\u0441\u043e\u0432 \u0432 \u0432\u043b ", None))
        self.set_up_button.setText(QCoreApplication.translate("MainWindow", u"\u043d\u0430\u0447\u0430\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0443", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0434\u0435\u0440\u0436\u043a\u0430 \u043c\u0435\u0436\u0434\u0443 \u0430\u043a\u043a\u0430\u043c\u0438", None))
        self.set_up_timeEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"mm:ss", None))
        self.change_password_checkbox.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043c\u0435\u043d\u0438\u0442\u044c \u043f\u0430\u0440\u043e\u043b\u044c", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.withdraw_address_input.setText(QCoreApplication.translate("MainWindow", u"\u0430\u0434\u0440\u0435\u0441 \u0432\u044b\u0432\u043e\u0434\u0430", None))
        self.launch_profile_btn.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u043a \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u043e\u0432", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0432\u043e\u0434", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0436\u0438\u043c \u0432\u044b\u0432\u043e\u0434\u0430", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0436\u0438\u043c 1", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0436\u0438\u043c 2", None))
        self.radioButton_3.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0436\u0438\u043c 3", None))
        self.launch_withdraw_btn.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c", None))
        self.withdraw_timeEdit.setDisplayFormat(QCoreApplication.translate("MainWindow", u"mm:ss", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u043e\u0439 \u043f\u0440\u043e\u043c\u0435\u0436\u0443\u0442\u043e\u043a \u043c\u0435\u0436\u0434\u0443 \u0430\u043a\u043a\u0430\u043c\u0438", None))
        self.data_btn.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0438\u043e\u043a \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u0439", None))
        self.data_time.setDisplayFormat(QCoreApplication.translate("MainWindow", u"mm:ss", None))
        self.chain_name_edit.setText(QCoreApplication.translate("MainWindow", u"\u0438\u043c\u044f \u0441\u0435\u0442\u0438", None))
        self.coin_edit.setText(QCoreApplication.translate("MainWindow", u"\u043c\u043e\u043d\u0435\u0442\u0430", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0432\u043e\u0434 \u0441 \u0431\u0438\u0440\u0436\u0438 \u043d\u0430 \u043a\u043e\u0448\u0435\u043b\u044c\u043a\u0438", None))
        self.min_amount_edit.setText(QCoreApplication.translate("MainWindow", u"\u043c\u0438\u043d\u0438\u043c\u0430\u043b\u044c\u043d\u043e\u0435 \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.random_range_edit_start.setText(QCoreApplication.translate("MainWindow", u"\u0440\u0430\u0437\u0431\u0440\u043e\u0441 \u0440\u0430\u043d\u0434\u043e\u043c\u0430", None))
        self.deposit_btn_launch.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0447\u0430\u0442\u044c \u0432\u044b\u0432\u043e\u0434", None))
        self.radioButton_4.setText(QCoreApplication.translate("MainWindow", u"Binance", None))
        self.random_range_edit_finish.setText(QCoreApplication.translate("MainWindow", u"\u0440\u0430\u0437\u0431\u0440\u043e\u0441 \u0440\u0430\u043d\u0434\u043e\u043c\u0430", None))
        self.gas_coin_amount_edit.setText(QCoreApplication.translate("MainWindow", u"\u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e gas coin", None))
        self.deposit_timer.setDisplayFormat(QCoreApplication.translate("MainWindow", u"mm:ss", None))
        self.symbol_edit.setText(QCoreApplication.translate("MainWindow", u"symbol", None))
        self.volume_edit.setText(QCoreApplication.translate("MainWindow", u"volume", None))
        self.launch_volume_btn.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0443\u0441\u0442\u0438\u0442\u044c", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0431\u0438\u0432\u0430\u043d\u0438\u0435 \u043e\u0431\u044a\u0435\u043c\u0430", None))
        self.volume_range_start.setText(QCoreApplication.translate("MainWindow", u"start", None))
        self.volume_range_finish.setText(QCoreApplication.translate("MainWindow", u"finish", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0438\u0430\u043f\u043e\u0437\u043e\u043d \u0440\u0430\u0437\u0431\u0440\u043e\u0441\u0430", None))
        self.volume_timer.setDisplayFormat(QCoreApplication.translate("MainWindow", u"mm:ss", None))
        self.volume_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0431\u0438\u0432\u0430\u0442\u044c \u043e\u0431\u044a\u0435\u043c", None))
        self.loan_checkBox.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0437\u044f\u0442\u044c \u0437\u0430\u0439\u043c", None))
        self.close_loan_chechbox.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c \u0432\u0441\u0435 \u0437\u0430\u0439\u043c\u044b", None))
        self.ts_edit.setText(QCoreApplication.translate("MainWindow", u"tokensplash code", None))
        self.register_in_st_btn.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0440\u0435\u0433\u0430\u0442\u044c", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044f \u0432 \u0442\u0441", None))
        self.ts_timer.setDisplayFormat(QCoreApplication.translate("MainWindow", u"mm:ss", None))
        self.btn_message.setText(QCoreApplication.translate("MainWindow", u"Message", None))
        self.btn_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"Fri3nd", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

