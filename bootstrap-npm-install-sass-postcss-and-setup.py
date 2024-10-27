import os
import shutil
import subprocess

# Run in the top level of a web dev project
# Installs Sass, PostCSS, and Bootstrap in node_modules
#   Installed Bootstrap to have access to its source files for customization
#   Installed Sass and PostCSS so we can run them as scripts from package.json
#   PostCSS needs browserslist property set within package.json file
# Adapts the package.json file so you can run Sass and PostCSS from the command line via npm
# $> npm run compile:sass
# $> npm run compile:sassmin
# $> npm run compile:prefix
# Python file created to run these npm commands consecutively
# Note: No npm for the latest Font Awesome version, so described manual install procedure

# Change a line in "file_name" containing "line_contains" to "line_new".
def change_line(file_name, line_contains, line_new1, line_new2):
    new_file = []
    with open(file_name, 'r') as file:
        for line in file:
            if line_contains in line:
                new_file.append(line_new1)
                new_file.append(line_new2)
            else:
                new_file.append(line)

    with open(file_name, 'w') as file:
        for line in new_file:
            file.write(line)

    print(f"...modified {file_name}")

def modify_package_json_scripts():
    file_name = "package.json"
    line_contains = "\"test\":"
    temp1 = "    \"compile:sass\": \"sass ./sass:./css/ --no-source-map\",\n    "
    line_new1 = temp1 + "\"compile:sassmin\": \"sass ./sass:./css/min/ --no-source-map --style compressed\","
    temp2 = "    \"compile:prefix\": \"postcss ./css/*.css --use autoprefixer --no-map -d ./css/prefixed/\",\n"
    temp3 = "    \"compile:prefixmin\": \"postcss ./css/min/*.css --use autoprefixer --no-map -d ./css/prefixedmin/\",\n"
    line_new2 = temp2 + temp3 + "    \"build:all\": \"run-s compile:sass compile:sassmin compile:prefix compile:prefixmin\""
    change_line(file_name, line_contains, line_new1, line_new2)

def modify_package_json_browser():
    file_name = "package.json"
    line_contains = "\"author\":"
    line_new1 = "  \"author\": \"\","
    line_new2 = "  \"browserslist\": \"last 4 versions\","
    change_line(file_name, line_contains, line_new1, line_new2)

# Rename JSON files 
if os.path.exists("package.json"):
    shutil.move("package.json", "package.json.prev")
if os.path.exists("package-lock.json"):
    shutil.move("package-lock.json", "package-lock.json.prev")

# Install npm-run-all (aka: run-s)
subprocess.run("npm i npm-run-all", shell=True)

# Initialize
subprocess.run("npm init -y", shell=True)

# Install Sass
subprocess.run("npm i sass", shell=True)

# Install Bootstrap
subprocess.run("npm i bootstrap@5.3.0", shell=True)

# FontAwesome (no npm for version 6)
# Manually downloaded "free for web" zip file from FontAwesome
# Now don't need to use the "cdn" kit
# Important: Must also copy the webfonts/ folder to the project root directory
# See portfolio-justit-version2/sass/fontawesome.scss:
# @use "../fontawesome-free-6.4.0-web/scss/brands.scss";
# @use "../fontawesome-free-6.4.0-web/scss/regular.scss";
# @use "../fontawesome-free-6.4.0-web/scss/fontawesome.scss";
# @use "../fontawesome-free-6.4.0-web/scss/solid.scss";
# Sass compile to ./css/fontawesome.css
# index.html: <link rel="stylesheet" href="./css/fontawesome.css">
# Copy webfonts/ dir to the project root dir too

# Install PostCSS and Autoprefixer
subprocess.run("npm install postcss postcss-cli autoprefixer", shell=True)

# Change package.json
modify_package_json_scripts()
modify_package_json_browser()

# Perl file to transpile all
perl_script_content = """
import subprocess
subprocess.run("npm run compile:sass", shell=True)
subprocess.run("npm run compile:sassmin", shell=True)
subprocess.run("npm run compile:prefix", shell=True)
subprocess.run("npm run compile:prefixmin", shell=True)
#subprocess.run("npm run compile:all", shell=True)
"""

perl_file_path = "./transpile-everything.py"
with open(perl_file_path, "w") as file:
    file.write(perl_script_content)
