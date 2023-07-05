import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Nested QVBoxLayout')
window.resize(300, 200)

main_layout = QVBoxLayout()
# main_layout.setSpacing(10)  # 设置主布局的子控件间距为 10 像素

sub_layout1 = QVBoxLayout()
sub_layout2 = QVBoxLayout()

# 添加子控件到子布局1
sub_layout1.addWidget(QLabel("子布局1中的控件1"))
sub_layout1.addWidget(QLabel("子布局1中的控件2"))

# 添加子控件到子布局2
sub_layout2.addWidget(QLabel("子布局2中的控件1"))
sub_layout2.addWidget(QLabel("子布局2中的控件2"))


# 添加子布局到主布局
main_layout.addLayout(sub_layout1)
main_layout.addLayout(sub_layout2)






window.setLayout(main_layout)
window.show()

sys.exit(app.exec())
