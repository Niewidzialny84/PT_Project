option_window_style = '''QMainWindow
{
	background: #000;
}
QPushButton
{
	background-color: #4d4d4d;
	color: #fff;
	radius: 10px;
	border-radius: 10px;
	border: 2px solid;
	outline: none;
    letter-spacing: 1px;
    height: 25px;
    margin: -2px 0px -2px 0px
}
QPushButton#password_Button
{
    height: 25px;
    margin: -2px 0px -2px 0px
}
QPushButton:hover
{
	background-color: #00DEA1;
    color: #000;
    border: 2px solid;
}
QPushButton#minimize_Button
{
    margin: 4px 4px 0px 0px;
}
QPushButton#quit_Button
{
	background-color: #800000;
    margin: 4px 4px 0px 0px;
    padding-left: 2px;
}
QPushButton#quit_Button:hover
{
	background-color: #cc0000;
    padding-left: 2px;
}
QLineEdit
{
    border-top-style: hidden;
    border-right-style: hidden;
    border-left-style: hidden;
    border-bottom-style: groove;
    background-color: #000;
    color: #fff;
    padding-left: 5px;
    border-bottom: 1px solid;
    border-color: #fff;
}
QLineEdit::PlaceholderText
{
    color: #4d4d4d;
}
QLabel
{
    color: #fff;
}
QFrame
{
    color: #fff;
}
QTextEdit
{
    border-radius: 10px;
	border: 2px solid;
    border-color: #fff;
    radius: 8px;
    color: #000; 
}
QLabel
{
    color: #fff;
    letter-spacing: 1px;
}
QComboBox
{
    border-radius: 10px;
	border: 2px solid;
    border-color: #fff;
    selection-background-color: #000;
    color: #fff;
    background-color: #000;
    padding-left: 5px;
}
QComboBox::drop-down
{
	border-right: 1px solid;
    border-color: #000;
    border-radius: 7px; 
}
QComboBox::down-arrow
{
    width: 0; 
    height: 0; 
    border-left: 5px solid #000;
    border-right: 5px solid #000;
    border-top: 5px solid #fff;
}
QComboBox::down-arrow:on
{
    width: 0; 
    height: 0; 
    border-top: 5px solid #000;
    border-bottom: 5px solid #000; 
    border-right: 5px solid #fff; 
}
QListView
{
    margin-top: 5px;
    color: #fff;
    border: 2px solid #fff;
    border-radius: 4px;
    selection-background-color: #00DEA1;
    selection-color: #000;
    background-color: #000;
    show-decoration-selected: 1; 
    outline: none;
}
'''

main_window_style = '''QMainWindow
{
	background: #000;
    color: #fff;
}
QPushButton
{
	background-color: #4d4d4d;
	color: #fff;
	radius: 10px;
	border-radius: 10px;
	border: 2px solid;
	outline: none;
    letter-spacing: 1px;
    height: 25px;
    margin: -2px 0px -2px 0px;
    padding: 0px;
}
QPushButton:hover
{
	background-color: #00DEA1;
    color: #000;
    border: 2px solid;
}
QPushButton#minimize_Button
{
    margin: 4px 4px 0px 0px;
}
QPushButton#quit_Button
{
	background-color: #800000;
    margin: 4px 4px 0px 0px;
    padding-left: 2px;
}
QPushButton#quit_Button:hover
{
	background-color: #cc0000;
    padding-left: 2px;
}
QLineEdit
{
    color: white;
    border-top-style: hidden;
    border-right-style: hidden;
    border-left-style: hidden;
    border-bottom-style: groove;
    background-color: #000;
    padding-left: 5px;
    border-bottom: 1px solid;
    border-color: #fff;
}
QLineEdit:focus
{
    color: white;
}
QLabel
{
    color: #fff;
}
QFrame
{
    color: #fff;
}
QTextEdit
{
    border-radius: 10px;
	border: 2px solid;
    border-color: #fff;
    radius: 8px;
    color: #000;
}
QTextEdit#chat_Enter_Field
{
    background-color: #cccccc;
}
QTextEdit#chat_Field
{
    background-color: #cccccc;
}
QLabel
{
    color: #fff;
    letter-spacing: 1px;
}
QLabel#chat_Limit
{
    margin-right: 2px;
    margin-bottom: 1px;
}
QListView
{
    border-radius: 10px;
	border: 2px solid;
    border-color: #fff;
    radius: 8px;
    background-color: #4d4d4d;
    padding: 0px 2px 0px 2px;
}
QListView:item:selected:active
{
    background-color: #00DEA1;
    color: black;
    border-radius: 8px;
}
QListView:item:hover
{
    background-color: #cccccc;
    color: black;
    border-radius: 8px;
}
QScrollBar:vertical 
{
	border: none;
    background: #000;
    width: 14px;
    margin: 15px 0 15px 0;
	border-radius: 0px;
    padding: 1px 0px 1px 0px;
 }
QScrollBar::handle:vertical 
{	
	background-color: #66ffd6;
	min-height: 35px;
	border-radius: 7px;
}
QScrollBar::handle:vertical:hover
{	
	background-color: #00dea1;
}
QScrollBar::handle:vertical:pressed 
{	
	background-color: #00b383;
}
QScrollBar::sub-line:vertical 
{
	border: none;
	background-color: #66ffd6;
	height: 15px;
	border-top-right-radius: 7px;
	subcontrol-position: top;
	subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:hover 
{	
	background-color: #00dea1;
}
QScrollBar::sub-line:vertical:pressed 
{	
	background-color: #00b383;
}
QScrollBar::add-line:vertical 
{
	border: none;
	background-color: #66ffd6;
	height: 15px;
	border-bottom-right-radius: 7px;
	subcontrol-position: bottom;
	subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:hover 
{	
	background: #00dea1;
}
QScrollBar::add-line:vertical:pressed 
{	
	background-color: #00b383;
}
QScrollBar::up-arrow:vertical  
{
    width: 0; 
    height: 0; 
    border-left: 5px solid #66ffd6;
    border-right: 5px solid #66ffd6;
    border-bottom: 5px solid #000;
}
QScrollBar::down-arrow:vertical
{
    width: 0; 
    height: 0; 
    border-left: 5px solid #66ffd6;
    border-right: 5px solid #66ffd6;
    border-top: 5px solid #000;
}
QScrollBar::up-arrow:vertical:pressed
{
    border-left: 5px solid #00b383;
    border-right: 5px solid #00b383;
}
QScrollBar::down-arrow:vertical:pressed
{
    border-left: 5px solid #00b383;
    border-right: 5px solid #00b383;
}
QScrollBar::up-arrow:vertical:hover 
{	
    border-left: 5px solid #00dea1;
    border-right: 5px solid #00dea1;
}
QScrollBar::down-arrow:vertical:hover 
{	
    border-left: 5px solid #00dea1;
    border-right: 5px solid #00dea1;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical 
{
	background: none;
}
'''

login_window_style ='''QMainWindow
{
	background: #000;
}
QPushButton
{
	background-color: #4d4d4d;
	color: #fff;
	radius: 10px;
	border-radius: 10px;
	border: 2px solid;
	outline: none;
    letter-spacing: 1px;
    height: 23px;
}
QPushButton:hover
{
	background-color: #00DEA1;
    color: #000;
    border: 2px solid;
}
QPushButton#minimize_Button
{
    margin: 4px 4px 0px 0px;
}
QPushButton#quit_Button
{
	background-color: #800000;
    margin: 4px 4px 0px 0px;
    padding-left: 2px;
}
QPushButton#quit_Button:hover
{
	background-color: #cc0000;
    padding-left: 2px;
}
QPushButton#language_Button
{
    margin-bottom: 1px;
}
QPushButton#login_Button
{
   margin-bottom: -2px;
}
QPushButton#forgot_Button
{
    margin-top: -2px;
    margin-bottom: 0px;
}
QLineEdit
{
    border-top-style: hidden;
    border-right-style: hidden;
    border-left-style: hidden;
    border-bottom-style: groove;
    background-color: #000;
    color: #fff;
    padding-left: 5px;
    border-bottom: 1px solid;
    border-color: #fff;
}
QLineEdit::PlaceholderText
{
    color: #4d4d4d;
}
QLabel
{
    color: #fff;
}
QFrame
{
    color: #fff;
}
'''

def get_login_window_style():
    return login_window_style

def get_main_window_style():
    return main_window_style

def get_settings_window_style():
    return option_window_style