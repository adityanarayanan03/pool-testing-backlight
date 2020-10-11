from cx_Freeze import setup, Executable


setup(name = 'Pool-Testing Backlight',
    version = '0.1',
    description='Program for pool-testing backlight',
    executables = [Executable("backlight.py")])