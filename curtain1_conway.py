nodes=['198948', '194947', '218370', '202949', '282455', '248143']
import itertools; s=nodes[4]; exec("for g in range(25):\n prev=len(s)\n s=''.join(str(len(list(grp)))+k for k,grp in itertools.groupby(s))"); ratio=len(s)/prev; print(f"1.CONWAY_AUDIOACTIVE_25: Start=282455 -> Gen25_Digits={len(s)} | GrowthRatio={ratio:.6f} (ConwayConstant=1.303577)")
