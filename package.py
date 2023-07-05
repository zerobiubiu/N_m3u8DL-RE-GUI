import sys
import platform
from PyInstaller.__main__ import run

current_os = platform.system()

if __name__ == '__main__':
    if current_os == 'Windows':
        icon_file = 'logo.ico'
    elif current_os == 'Darwin':
        icon_file = 'logo.icns'
    elif current_os == 'Linux':
        icon_file = 'logo.png'
    else:
        icon_file = 'logo.png'
    # 设置打包参数
    opts = ['--windowed',  '--hidden-import=desktop_notifier.resources', '--name', 'N_m3u8DL-RE-GUI', '--icon=./logo/'+icon_file,
            'index.py', '-w', '--add-binary', './bin/*:./bin/']

    # 执行打包
    run(opts)
