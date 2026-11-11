nodes=['194947', '218370', '202949', '282455', '248143', '198948']
import sys; sys.setrecursionlimit(100000); exec("def A(m, n):\n if m==0: return n+1\n if m>0 and n==0: return A(m-1, 1)\n return A(m-1, A(m, n-1))"); res=A(4, 1); print(f"Ackermann Limit: A(4, 1) = {res}")
