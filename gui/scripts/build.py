#!/usr/bin/env python3
import shutil
from subprocess import run

run(["python", "-m", "PyInstaller", "app.spec", "--noconfirm"])
shutil.copytree("assets/", "dist/app/assets", dirs_exist_ok=True)
shutil.copytree("qml/", "dist/app/qml", dirs_exist_ok=True)
