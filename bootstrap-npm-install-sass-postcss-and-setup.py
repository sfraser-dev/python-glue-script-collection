import subprocess
import os
import pathlib

# Rename JSON files
if os.path.exists("package.json"):
    os.rename("package.json", "package.json.prev")

if os.path.exists("package-lock.json"):
    os.rename("package-lock.json", "package-lock.json.prev")

# Install npm-run-all
subprocess.run(["npm", "install", "npm-run-all"])

# Initialize npm
subprocess.run(["npm", "init", "-y"])

# Install Sass
subprocess.run(["npm", "install", "sass"])

# Install Bootstrap
subprocess.run(["npm", "install", "bootstrap@5.3.0"])

# Install PostCSS and Autoprefixer
subprocess.run(["npm", "install", "postcss", "postcss-cli", "autoprefixer"])

# Modify package.json
modify_package_json_scripts()
modify_package_json_browser()

# Create Perl file to transpile all
transpile_all_file = """
#!/usr/bin/python

import subprocess

subprocess.run(["npm", "run", "compile:sass"])
subprocess.run(["npm", "run", "compile:sassmin"])
subprocess.run(["npm", "run", "compile:prefix"])
subprocess.run(["npm", "run", "compile:prefixmin"])
# subprocess.run(["npm", "run", "build:all"])
"""

with open("transpile-everything.pl", "w") as f:
    f.write(transpile_all_file)

def modify_package_json_scripts():
    package_json_path = pathlib.Path("package.json")
    package_json_content = package_json_path.read_text()

    new_package_json_content = package_json_content.replace(
        '"test":',
        '  "compile:sass": "sass ./sass:./css/ --no-source-map",\n  '
    )
    new_package_json_content = new_package_json_content.replace(
        '  "scripts": {',
        '  "scripts": {\n    "compile:sassmin": "sass ./sass:./css/min/ --no-source-map --style compressed",\n    '
    )
    new_package_json_content = new_package_json_content.replace(
        '      "build": "run-s dev server"   }',
        '      "build": "run-s compile:sass compile:sassmin compile:prefix compile:prefixmin"   }\n    }'
    )

    package_json_path.write_text(new_package_json_content)
    print("...modified package.json")

def modify_package_json_browser():
    package_json_path = pathlib.Path("package.json")
    package_json_content = package_json_path.read_text()

    new_package_json_content = package_json_content.replace(
        '"author":',
        '  "author": "",\n  '
    )
    new_package_json_content = new_package_json_content.replace(
        '  "dependencies": {',
        '  "dependencies": {\n    "browserslist": "last 4 versions",\n  }'
    )

    package_json_path.write_text(new_package_json_content)
    print("...modified package.json")

# Run transpile-everything.pl
subprocess.run(["python", "transpile-everything.pl"])

