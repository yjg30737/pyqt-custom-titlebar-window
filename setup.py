from setuptools import setup, find_packages

setup(
    name='pyqt-custom-titlebar-window',
    version='0.7.0',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt Custom Titlebar Window (resizable, movable, minimize/maximize/close)',
    url='https://github.com/yjg30737/pyqt-custom-titlebar-window.git',
    install_requires=[
        'PyQt5>=5.15',
        'pyqt-frameless-window @ git+https://git@github.com/yjg30737/pyqt-frameless-window.git@main',
        'python-color-getter @ git+https://git@github.com/yjg30737/python-color-getter.git@main'
    ]
)