import sys
import os
import subprocess
import asyncio
import shutil
from desktop_notifier import DesktopNotifier
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QSpinBox, QPushButton, QTextEdit, QFileDialog, QMessageBox
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QFont

current_dir = os.path.dirname(os.path.abspath(__file__))
cli_path = os.path.join(current_dir, 'bin/N_m3u8DL-RE')


class PlainTextEdit(QTextEdit):
    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())


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
input_textedit = PlainTextEdit()
input_layout = QVBoxLayout()
input_layout.addWidget(input_label)
input_layout.addWidget(input_textedit)
layout.addLayout(input_layout)

# save-name
save_name_label = QLabel('保存文件名')
save_name_label.setAlignment(Qt.AlignCenter)
save_name_textedit = PlainTextEdit()
save_name_layout = QVBoxLayout()
save_name_layout.addWidget(save_name_label)
save_name_layout.addWidget(save_name_textedit)
layout.addLayout(save_name_layout)

bottom_layout = QHBoxLayout()

left_layout = QVBoxLayout()
right_layout = QVBoxLayout()

ffmpeg_dir_label = QLabel('ffmpeg选择')
ffmpeg_dir_input = QLineEdit(shutil.which("ffmpeg"))
ffmpeg_dir_button = QPushButton('选择ffmpeg')
ffmpeg_dir_layout = QHBoxLayout()
ffmpeg_dir_layout.addWidget(ffmpeg_dir_label)
ffmpeg_dir_layout.addWidget(ffmpeg_dir_input)
ffmpeg_dir_layout.addWidget(ffmpeg_dir_button)
left_layout.addLayout(ffmpeg_dir_layout)


def on_ffmpeg_button_clicked():
    dir_name, _ = QFileDialog.getOpenFileName(window, '选择ffmpeg文件')
    if dir_name:
        ffmpeg_dir_input.setText(dir_name)


ffmpeg_dir_button.clicked.connect(on_ffmpeg_button_clicked)

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

log_dir_label = QLabel('日志目录')
log_dir_input = QLineEdit(save_dir_input.text()+'log')
log_dir_button = QPushButton('选择目录')
log_dir_layout = QHBoxLayout()
log_dir_layout.addWidget(log_dir_label)
log_dir_layout.addWidget(log_dir_input)
log_dir_layout.addWidget(log_dir_button)
left_layout.addLayout(log_dir_layout)


def on_log_dir_button_clicked():
    dir_name = QFileDialog.getExistingDirectory(window, '选择目录')
    if dir_name:
        log_dir_input.setText(dir_name)


log_dir_button.clicked.connect(on_log_dir_button_clicked)


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
run_button.setFont(QFont("Arial", 28))
run_button.setFixedHeight(100)


def on_run_button_clicked():
    if not input_textedit.toPlainText():
        QMessageBox.warning(window, '警告', '下载链接不能为空!')
        return
    if not save_dir_input.text():
        QMessageBox.warning(window, '警告', '输出目录不能为空!')
        return
    if not ffmpeg_dir_input.text():
        QMessageBox.warning(window, '警告', 'ffmpeg不能为空!')
        return

    inputs = input_textedit.toPlainText().split('\n')
    save_names = save_name_textedit.toPlainText().split('\n')

    # Check and create the log directory if it exists
    if log_dir_input.text():
        os.makedirs(log_dir_input.text(), exist_ok=True)

    for i, input_str in enumerate(inputs):
        if not input_str:
            continue

        cmd_str = [input_str]

        if tmp_dir_input.text():
            cmd_str.extend(['--tmp-dir', tmp_dir_input.text()])

        if save_dir_input.text():
            cmd_str.extend(['--save-dir', save_dir_input.text()])

        if ffmpeg_dir_input.text():
            cmd_str.extend(['--ffmpeg-binary-path', ffmpeg_dir_input.text()])

        if i < len(save_names) and save_names[i]:
            cmd_str.extend(['--save-name', save_names[i]])
        else:
            cmd_str.extend(
                ['--save-name', QDateTime.currentDateTime().toString("yyyyMMddhhmmss")])

        cmd_str.extend(['--thread-count', str(thread_count_input.value())])

        if log_dir_input.text():
            log_file_path = log_dir_input.text()+"/" + \
                QDateTime.currentDateTime().toString(
                    'yyyyMMddhhmmss')+"-"+cmd_str[8]+".log"
            with open(log_file_path, 'w') as f:
                result = subprocess.run(
                    [cli_path] + cmd_str, capture_output=True, text=True)
                f.write(result.stdout)
                f.write(result.stderr)
        else:
            cmd_str.append('--no-log')
            result = subprocess.run([cli_path] + cmd_str,
                                capture_output=True, text=True)
        if result.returncode == 0:
            asyncio.run(send_notification("下载完成", cmd_str[8] + " 下载成功"))
        else:
            asyncio.run(send_notification("下载失败", cmd_str[8] + " 下载失败"))


run_button.clicked.connect(on_run_button_clicked)

right_layout.addWidget(run_button)

bottom_layout.addLayout(left_layout)
bottom_layout.addLayout(right_layout)

layout.addLayout(bottom_layout)

window.setLayout(layout)
window.show()

sys.exit(app.exec())
