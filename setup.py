from setuptools import setup, find_packages

setup(
    name='pyqt-custom-frame',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt custom frame',
    url='https://github.com/yjg30737/pyqt-custom-frame.git',
    install_requires=[
        'PyQt5>=5.15'
    ]
)