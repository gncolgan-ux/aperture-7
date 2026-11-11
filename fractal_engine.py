nodes=['198948', '194947', '218370', '202949', '282455', '248143']
exec("w,h=60,30\nfor y in range(h):\n s=''\n for x in range(w):\n  c=complex(2.5*x/w-2.0, 2.5*y/h-1.25)\n  z=0j\n  for i in range(50):\n   if abs(z)>2: break\n   z=z*z+c\n  s+='@' if i==49 else ' '\n print(s)")
