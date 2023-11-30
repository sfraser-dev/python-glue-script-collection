import os
import subprocess

def modify_tailwind_config_js_and_fix_formatting():
    file_name = "tailwind.config.js"

    with open(file_name, 'w') as f:
        f.write("""/** \@type {import('tailwindcss').Config} */

module.exports = {

  content: ["./**/*.{html,js}"],
  theme: {

    extend: {},

  },

  plugins: [],

};""")

    print(f"...modified {file_name} and fixed formatting")

def modify_tailwind_config_js():
    file_name = "tailwind.config.js"
    line_contains = "content"
    line_new = "content: [\"./**/*.{html,js}\"],"

    change_line(file_name, line_contains, line_new)

def modify_package_json():
    file_name = "package.json"
    line_contains = "\"test\":"
    line_new = "  \"build-css\": \"npx tailwindcss -i ./tailwind/tailwind.css -o ./css/style.css --watch\""

    change_line(file_name, line_contains, line_new)

def change_line(file_name, line_contains, line_new):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line_contains in line:
            lines[i] = line_new

    with open(file_name, 'w') as f:
        f.writelines(lines)

    print(f"...modified {file_name}")

def populate_with_boilerplate(file_name):
    with open(file_name, 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="./css/style.css">
<title>Document</title>
</head>
<body>
  <h1 class="bg-green-500">tailwind test</h1>
</body>
</html>""")

    print(f"...boilerplate added to {file_name}")

def populate_with_tailwind_directives(file_name):
    with open(file_name, 'w') as f:
        f.write("""@tailwind base;
@tailwind components;
@tailwind utilities;""")

    print(f"...tailwind directives added to {file_name}")

def populate_with_npm_command(file_name):
    with open(file_name, 'w') as f:
        f.write("""#!/usr/bin/python

import subprocess

subprocess.call(["npm", "run", "build-css"])
""")

    print(f"...npm command added to {file_name}")

if __name__ == "__main__":
    os.makedirs("./css", exist_ok=True)
    os.makedirs("./tailwind", exist_ok=True)

    populate_with_boilerplate("./index.html")
    populate_with_tailwind_directives("./tailwind/tailwind.css")
    populate_with_npm_command("./watcher-restart.py")

    subprocess.call(["npm", "init", "-y"])
    subprocess.call(["npm", "install", "-D", "tailwindcss"])
    subprocess.call(["npx", "tailwindcss", "init"])

    modify_tailwind_config_js_and_fix_formatting()
    modify_package_json()

    subprocess.call(["npx", "tailwindcss", "-i", "./tailwind/tailwind.css", "-o", "./css/style.css", "--watch"])

