nodes=['194947', '218370', '202949', '282455', '248143', '198948']
import math; v=[float(x) for x in nodes]; heat_flux=sum((math.sin(x)*math.log(x)) for x in v); fracture_mach=abs(heat_flux) * math.pi + 15.0; print(f"PTFE_Casing_Integrity: Max Heat Flux={heat_flux:.4f} | Structural Failure at Mach {fracture_mach:.2f}")
