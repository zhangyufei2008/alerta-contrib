
from setuptools import setup, find_packages

version = '7.0.0'

setup(
    name="alerta-checkup",
    version=version,
    description='Alerta plugin for checkup health',
    url='https://github.com/zhangyufei2008/alerta-contrib.git',
    license='MIT',
    author='Nick Satterly',
    author_email='zhang-yufei-2008@163.com',
    packages=find_packages(),
    py_modules=['alerta_checkup'],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.plugins': [
            'debug = alerta_checkup:CheckUp'
        ]
    },
    python_requires='>=3.5'
)
