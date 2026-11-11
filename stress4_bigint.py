nodes=['198948', '194947', '218370', '202949', '282455', '248143']
import math; v=[int(x) for x in nodes]; P=(10**9)+7; acc=v[4]; exec("for i in range(10000):\n acc=pow(acc, v[i%6], P) ^ (v[(i+3)%6]*i)"); big=math.prod(x**50 for x in v); print(f"4.BIGINT_AVALANCHE: 10k_Modular_Cascade={acc} | Exact_300_Power_Digits={len(str(big))} | Top12Digits={str(big)[:12]}")
