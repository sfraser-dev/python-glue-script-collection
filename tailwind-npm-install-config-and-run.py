import os

def modify_tailwind_config_js_and_fix_formatting():
    file_name = "tailwind.config.js"
    
    str_content = """/** @type {import('tailwindcss').Config} */

module.exports = {

    content: ["./**/*.{html,js}"],
    theme: {

        extend: {},

    },

    plugins: [],

};"""

    with open(file_name, 'w') as fh:
        fh.write(str_content)

    print(f"...modified {file_name} and fixed formatting")

def modify_tailwind_config_js():
    file_name = "tailwind.config.js"
    line_contains = "content"
    line_new = "content: [\"./**/*.{html,js}\"],"

    change_line(file_name, line_contains, line_new)

def modify_package_json():
    file_name = "package.json"
    line_contains = "\"test\":"
    line_new = "    \"build-css\": \"npx tailwindcss -i ./tailwind/tailwind.css -o ./css/style.css --watch\""

    change_line(file_name, line_contains, line_new)

def change_line(file_name, line_contains, line_new):
    new_file = []
    
    with open(file_name, 'r') as fh:
        for line in fh:
            if line_contains in line:
                new_file.append(line_new)
            else:
                new_file.append(line)

    with open(file_name, 'w') as fh:
        for line in new_file:
            fh.write(line)

    print(f"...modified {file_name}")

def populate_with_boilerplate(file_name):
    str_content = """<!DOCTYPE html>
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
</html>"""

    with open(file_name, 'w') as fh:
        fh.write(str_content)

    print(f"...boilerplate added to {file_name}")

def populate_with_tailwind_directives(file_name):
    arr = [
        "@tailwind base;",
        "@tailwind components;",
        "@tailwind utilities;"
    ]

    with open(file_name, 'w') as fh:
        for line in arr:
            fh.write(line + '\n')

    print(f"...tailwind directives added to {file_name}")

def populate_with_npm_command(file_name):
    with open(file_name, 'w') as fh:
        fh.write("import subprocess\n")
        fh.write("subprocess.run(['npm', 'run', 'build-css'], check=True, shell=True)")
    print(f"...npm command added to {file_name}")

if __name__ == "__main__":
    print("\n\nRun in a new / clean directory\n\n")
    
    os.makedirs("./css", exist_ok=True)
    os.makedirs("./tailwind", exist_ok=True)

    populate_with_boilerplate("./index.html")
    populate_with_tailwind_directives("./tailwind/tailwind.css")
    populate_with_npm_command("./watcher-restart.py")

    os.system("npm init -y")
    os.system("npm install -D tailwindcss")
    os.system("npx tailwindcss init")

    modify_tailwind_config_js_and_fix_formatting()
    modify_package_json()

    os.system("npx tailwindcss -i ./tailwind/tailwind.css -o ./css/style.css --watch")
