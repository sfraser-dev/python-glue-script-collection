import subprocess
import os

# compile to get .o object files
subprocess.run(["clang++", "-c", "test.cpp", "test-joe.cpp"])

# link files to produce .exe
subprocess.run(["clang++", "test.o", "test-joe.o", "-o", "test-exe-file.exe"])

# get the full path name of the executable
cwd = os.getcwd()
exe = os.path.join(cwd, "test-exe-file.exe")

# run exe, store program output in variable (hidden by default when run from Python file)
output = subprocess.check_output(exe, shell=True, text=True)

# print exe output to screen
print(output)