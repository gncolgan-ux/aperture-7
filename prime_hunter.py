nodes=['198948', '194947', '218370', '202949', '282455', '248143']
import time; target=39999994400001711; t0=time.time(); exec("f=0\nfor i in range(3, int(target**0.5)+1, 2):\n if target%i==0:\n  f=i\n  break"); print(f"RSA_Target={target} | Prime_Factor={f} | Time={time.time()-t0:.2f}s | Divisions_Run={(f//2):,}")
