import sys, os, subprocess

z0 = [224782, 202949, 282455, 248143, 198948, 194947, 218370]
env = {"$C0": str(z0[0]), **{f"$E{i}": str(z0[i+1]) for i in range(6)}, "$REG": "0x3F_SYNCED"}
imp, sh = [], 0

def run_line(l):
    global sh, z0
    for k, v in env.items(): l = l.replace(k, v)
    print(f"[HX-EXEC] {l}")
    if l.startswith("Shift("):
        sh = int(l[6:-1]) % 6
        edges = z0[1:][-sh:] + z0[1:][:-sh] if sh else z0[1:]
        for i in range(6): env[f"$E{i}"] = str(edges[i])
    elif l.startswith("Query("):
        q = l[6:-1]
        vals = [int(env[f"$E{i}"]) for i in range(6)]
        peak = vals.index(max(vals))
        spread = max(vals) - min(vals)
        env["$REG"] = f"Q:'{q}' | Peak:E{peak}({max(vals)}) | Spread:{spread} | C0:{env['$C0']}"
        print(f"[HX-ANS]  {env['$REG']}")
    elif l.startswith("Imprint("): imp.append(l[8:-1])
    elif l.startswith("Exec("):
        fn = l[5:-1].strip()
        code = imp[-1].replace("import h3, pyroomacoustics as pra;", "").strip() if imp else "print('OK')"
        open(fn, "w").write(f"nodes={[env[f'$E{i}'] for i in range(6)]}\n{code}\n")
        env["$REG"] = subprocess.check_output(["python3", fn], text=True).strip()
        print(f"[HX-OUT]  {env['$REG']}")

if os.path.isfile(sys.argv[1]):
    for line in open(sys.argv[1]):
        if line.strip() and not line.startswith("#"): run_line(line.strip())
else:
    run_line(f"Query({' '.join(sys.argv[1:])})")
