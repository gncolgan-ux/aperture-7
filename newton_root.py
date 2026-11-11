nodes=['194947', '218370', '202949', '282455', '248143', '198948']
v="".join(nodes); n=int(v); x=n; exec("while True:\n y=(x+n//x)//2\n if y>=x: break\n x=y"); print(f"Node_Singularity={n} | Exact_Int_Root={x} | Remainder={n-x**2}")
