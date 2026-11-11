nodes=['248143', '198948', '194947', '218370', '202949', '282455']
v=[float(x) for x in nodes]; n=int((sum(v)*100)%10000) + 837799; start=n; steps=0; peak=n; exec("while n!=1:\n if n%2==0:\n  n=n//2\n else:\n  n=3*n+1\n steps+=1\n if n>peak: peak=n"); print(f"Collatz Chaos: Start_Seed={start} | Steps_to_1={steps} | Peak_Altitude={peak:,}")
