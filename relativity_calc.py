nodes=['218370', '202949', '282455', '248143', '198948', '194947']
import math; v=[float(x) for x in nodes]; c=299792458.0; mass=v[0]; vel=v[4]*1000; lorentz=1/math.sqrt(1-(vel**2/c**2)); ke=(lorentz-1)*mass*c**2; print(f"Relativistic_KE={ke:.4e}_Joules | Lorentz_Factor={lorentz:.15f}")
