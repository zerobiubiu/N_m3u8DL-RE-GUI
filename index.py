import sys
import os
import subprocess
import asyncio
from desktop_notifier import DesktopNotifier
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QCheckBox, QSpinBox, QComboBox, QPushButton, QTextEdit, QFileDialog, QMessageBox
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QFont

current_dir = os.path.dirname(os.path.abspath(__file__))
cli_path = os.path.join(current_dir, 'bin/N_m3u8DL-RE')


async def send_notification(title, text):
    notifier = DesktopNotifier()
    await notifier.send(title, text)

app = QApplication(sys.argv)

window = QtWidgets.QWidget()
window.setWindowTitle('N_m3u8DL-CLI-RE GUI')
window.resize(700, 450)

layout = QVBoxLayout()

# input
input_label = QLabel('下载链接')
input_label.setAlignment(Qt.AlignCenter)
input_textedit = QTextEdit()
input_layout = QVBoxLayout()
input_layout.addWidget(input_label)
input_layout.addWidget(input_textedit)
layout.addLayout(input_layout)

# save-name
save_name_label = QLabel('保存文件名')
save_name_label.setAlignment(Qt.AlignCenter)
save_name_textedit = QTextEdit()
save_name_layout = QVBoxLayout()
save_name_layout.addWidget(save_name_label)
save_name_layout.addWidget(save_name_textedit)
layout.addLayout(save_name_layout)

bottom_layout = QHBoxLayout()

left_layout = QVBoxLayout()
right_layout = QVBoxLayout()

# tmp-dir
tmp_dir_label = QLabel('临时文件存储目录')
tmp_dir_input = QLineEdit('/tmp/N_m3u8DL-RE')
tmp_dir_button = QPushButton('选择目录')
tmp_dir_layout = QHBoxLayout()
tmp_dir_layout.addWidget(tmp_dir_label)
tmp_dir_layout.addWidget(tmp_dir_input)
tmp_dir_layout.addWidget(tmp_dir_button)
left_layout.addLayout(tmp_dir_layout)


def on_tmp_dir_button_clicked():
    dir_name = QFileDialog.getExistingDirectory(window, '选择目录')
    if dir_name:
        tmp_dir_input.setText(dir_name)


tmp_dir_button.clicked.connect(on_tmp_dir_button_clicked)

# save-dir
save_dir_label = QLabel('输出目录')
save_dir_input = QLineEdit(os.path.expanduser("~")+'/Downloads/')
save_dir_button = QPushButton('选择目录')
save_dir_layout = QHBoxLayout()
save_dir_layout.addWidget(save_dir_label)
save_dir_layout.addWidget(save_dir_input)
save_dir_layout.addWidget(save_dir_button)
left_layout.addLayout(save_dir_layout)


def on_save_dir_button_clicked():
    dir_name = QFileDialog.getExistingDirectory(window, '选择目录')
    if dir_name:
        save_dir_input.setText(dir_name)


save_dir_button.clicked.connect(on_save_dir_button_clicked)

# thread-count
thread_count_label = QLabel('下载线程数')
thread_count_input = QSpinBox()
thread_count_input.setValue(16)
thread_count_input.setMinimum(1)
thread_count_layout = QHBoxLayout()
thread_count_layout.addWidget(thread_count_label)
thread_count_layout.addWidget(thread_count_input)
right_layout.addLayout(thread_count_layout)

run_button = QPushButton('启动下载')
run_button.setFont(QFont("Arial", 14))
run_button.setFixedHeight(50)


def on_run_button_clicked():
    if not input_textedit.toPlainText():
        QMessageBox.warning(window, '警告', '下载链接不能为空!')
        return
    if not save_dir_input.text():
        QMessageBox.warning(window, '警告', '输出目录不能为空!')
        return
    # Collect the values from the GUI elements and build the command line string.
    inputs = input_textedit.toPlainText().split('\n')
    save_names = save_name_textedit.toPlainText().split('\n')
    for i, input_str in enumerate(inputs):
        cmd_str = []
        if not input_str:
            continue
        cmd_str.append(input_str)
        if tmp_dir_input.text():
            cmd_str.append('--tmp-dir')
            cmd_str.append(tmp_dir_input.text())
        if save_dir_input.text():
            cmd_str.append('--save-dir')
            cmd_str.append(save_dir_input.text())
        if i < len(save_names) and save_names[i]:
            cmd_str.append('--save-name')
            cmd_str.append(save_names[i])
        else:
            cmd_str.append('--save-name')
            cmd_str.append(
                QDateTime.currentDateTime().toString("yyyyMMddhhmmss"))
        cmd_str.append('--thread-count')
        cmd_str.append(str(thread_count_input.value()))
        cmd_str.append('--no-log')

        result = subprocess.run([cli_path]+cmd_str)
        if result.returncode == 0:
            asyncio.run(send_notification("下载完成", cmd_str[6]+" 下载成功"))
        else:
            asyncio.run(send_notification("下载失败", cmd_str[6]+" 下载失败"))


run_button.clicked.connect(on_run_button_clicked)

right_layout.addWidget(run_button)

bottom_layout.addLayout(left_layout)
bottom_layout.addLayout(right_layout)

layout.addLayout(bottom_layout)

window.setLayout(layout)
window.show()

sys.exit(app.exec())
