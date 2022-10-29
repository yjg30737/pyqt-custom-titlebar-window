from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name='pyqt-custom-titlebar-window',
    version='0.0.47',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt custom titlebar window (resizable, movable, minimize/maximize/close, etc.)',
    url='https://github.com/yjg30737/pyqt-custom-titlebar-window.git',
    long_description_content_type='text/markdown',
    long_description=long_description,
    install_requires=[
        'PyQt5>=5.15',
        'pyqt-frameless-window==0.0.61',
        'pyqt-windows-buttons-widget>=0.0.1',
        'pyqt-mac-buttons-widget>=0.0.1',
        'pyqt-top-titlebar-widget>=0.0.1',
        'pyqt-svg-label>=0.0.1'
    ]
)