from setuptools import setup, find_namespace_packages

setup(
    name='bot',
    version='0.1.0',
    description='Personal Assistant from phonebook and notes',
    url='https://github.com/maracasabat/Personal-Assistant',
    author='Ivan Yevpat, Александра Болдышева. Марк Подопригора',
    author_email='maracasabat@gmail.com, 44darkos@gmail.com, sash_01@icloud.com',
    license='MIT',
    install_requires=['pick==1.2.0'],
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ],
    packages=find_namespace_packages(),
    entry_points={'console_scripts': [
        'bot=Personal_assistant.main:main']}
)