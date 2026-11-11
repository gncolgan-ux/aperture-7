nodes=['202949', '282455', '248143', '198948', '194947', '218370']
v=[float(i) for i in nodes]; m=max(v); x,y,z=v[0]/m,v[1]/m,v[2]/m; exec("for _ in range(250000):\n dx=10*(y-x)*0.001\n dy=(x*(28-z)-y)*0.001\n dz=(x*y-(8.0/3.0)*z)*0.001\n x+=dx; y+=dy; z+=dz"); print(f"Lorenz Chaos Anchor: X={x:.6f} | Y={y:.6f} | Z={z:.6f}")
