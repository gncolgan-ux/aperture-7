with open("hx_vm.cpp", "r") as f:
    code = f.read()

# If hx_vm.cpp got overwritten by the half-paste, restore from a clean compact build
import subprocess, sys
