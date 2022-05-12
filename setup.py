from setuptools import setup, find_packages

setup(
    name='pyqt-custom-titlebar-window',
    version='1.7.7',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt Custom Titlebar Window (resizable, movable, minimize/maximize/close)',
    url='https://github.com/yjg30737/pyqt-custom-titlebar-window.git',
    install_requires=[
        'PyQt5>=5.15',
        'pyqt-frameless-window>=0.0.1',
        'pyqt-windows-buttons-widget>=0.0.1',
        'pyqt-mac-buttons-widget>=0.0.1',
        'pyqt-top-titlebar-widget>=0.0.1',
        'python-get-absolute-resource-path>=0.0.1'
    ]
)