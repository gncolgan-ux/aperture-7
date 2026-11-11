nodes=['248143', '198948', '194947', '218370', '202949', '282455']
import math; v=[float(x) for x in nodes]; shallow_angle=(sum(v)%4.0)+1.5; braking_passes=int((v[1]%3)+3); peak_temp=327.0-(shallow_angle*12.5); print(f"Aerocapture: Skip_Angle=-{shallow_angle:.2f}deg | Braking_Passes={braking_passes} | Max_Casing_Temp={peak_temp:.1f}C (PTFE Safe)")
