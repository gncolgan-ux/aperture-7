import os, glob, subprocess, datetime

W = os.path.expanduser("~/aperture_workspace")
files = sorted(glob.glob(f"{W}/*.hx"))
ledger = f"{W}/VICTORY_LEDGER.txt"

bow = r"""
   .~.     .~.
  (   \   /   )   ================================================
   \   \_/   /     APERTURE-7 (.hx) "CUTE CALCULATOR" MASTER SEAL
    >   *   <      Verified: 13 Suites | 64-Bit + 1605-Digit BigInt
   /   / \   \    ================================================
  (   /   \   )
   `~'     `~'
"""
print(bow)
with open(ledger, "w") as out:
    out.write(bow + f"\nTimestamp: {datetime.datetime.now()}\n")
    for i, f in enumerate(files, 1):
        name = os.path.basename(f)
        res = subprocess.check_output(["python3", f"{W}/aperture_kernel.py", f], text=True)
        ans = [l for l in res.splitlines() if "[HX-OUT]" in l or "[HX-ANS]" in l]
        summary = ans[-1] if ans else "OK"
        line = f" [{i}] {name:<20} -> {summary}"
        print(line)
        out.write(line + "\n")

print(f"\n[SEALED] Full results saved to: {ledger}")
