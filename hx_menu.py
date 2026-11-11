import os, glob, subprocess, sys

W = os.path.expanduser("~/aperture_workspace")
files = sorted(glob.glob(f"{W}/*.hx"))

print("\n=== APERTURE-7 (.hx) MASTER WORKSPACE ===")
for i, f in enumerate(files, 1):
    name = os.path.basename(f)
    lines = [l.strip() for l in open(f) if l.strip() and not l.startswith("#")]
    preview = lines[-1] if lines else "Empty"
    print(f" [{i}] {name:<20} ({len(lines)} cmds) | Last: {preview[:40]}")

print("\nUsage:")
print("  hx-list          -> Show this indexed menu")
print("  hx-list <num>    -> Run script by number (e.g., 'hx-list 1')")
print("  hx-list all      -> Run every .hx benchmark suite in sequence\n")

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == "all":
        for f in files:
            print(f"\n>>> RUNNING: {os.path.basename(f)} <<<")
            subprocess.run(["python3", f"{W}/aperture_kernel.py", f])
    elif arg.isdigit() and 1 <= int(arg) <= len(files):
        target = files[int(arg)-1]
        print(f"\n>>> RUNNING: {os.path.basename(target)} <<<")
        subprocess.run(["python3", f"{W}/aperture_kernel.py", target])
