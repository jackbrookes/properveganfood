"""
Generates static HTML by walking over all URLs.
"""

from flask_frozen import Freezer
from app import application
import os

# set WD to this folder
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

application.config["FREEZER_DESTINATION_IGNORE"] = [
    "source/", ".vscode/", ".git", ".gitignore", "README.md"]

application.config["FREEZER_DESTINATION"] = "./../.."

freezer = Freezer(application)

if __name__ == '__main__':
    freezer.freeze()
