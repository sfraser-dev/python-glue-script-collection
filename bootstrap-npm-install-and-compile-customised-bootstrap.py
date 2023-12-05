import subprocess
import os
import pathlib

# Install Bootstrap using npm
subprocess.check_call("npm init -y", shell=True)
subprocess.check_call("npm install bootstrap@5.3.0", shell=True)

# Create customized_bootstrap.scss file
customized_bootstrap_scss = """
$primary: pink;
$secondary: green;
@import "../node_modules/bootstrap/scss/bootstrap";
"""

sass_dir = pathlib.Path("./sass/")
sass_dir.mkdir(parents=True, exist_ok=True)

customized_bootstrap_scss_path = sass_dir / "customized_bootstrap.scss"
with open(customized_bootstrap_scss_path, "w") as f:
    f.write(customized_bootstrap_scss)

# Compile Bootstrap using Sass with our customizations
css_dir = pathlib.Path("./css/")
css_dir.mkdir(parents=True, exist_ok=True)

subprocess.check_call("sass ./sass/customized_bootstrap.scss ./css/customized_bootstrap.css --no-source-map", shell=True)
subprocess.check_call("sass ./sass/customized_bootstrap.scss ./css/customized_bootstrap.min.css --style compressed --no-source-map", shell=True)

# Write a Python file to compile Bootstrap in the same folder as our customized.scss file
customized_bootstrap_pl = """
import subprocess
import os
import pathlib

sass_dir = pathlib.Path("./sass/")
css_dir = pathlib.Path("./css/")

subprocess.check_call("sass ./customized_bootstrap.scss ./css/customized_bootstrap.css --no-source-map", shell=True)
subprocess.run("sass ./customized_bootstrap.scss ./css/customized_bootstrap.min.css --style compressed --no-source-map", shell=True)
"""

customized_bootstrap_pl_path = sass_dir / "customized_bootstrap.pl"
with open(customized_bootstrap_pl_path, "w") as f:
    f.write(customized_bootstrap_pl)

# Start Chrome using our customized Bootstrap CSS file and a test HTML file
current_dir = os.getcwd()
html_file_full_path = os.path.join(current_dir, "bootstrap-npm-install-and-compile-customised-bootstrap-test-sample.html")
print(html_file_full_path)
subprocess.check_call(f"start chrome {html_file_full_path}", shell=True)

