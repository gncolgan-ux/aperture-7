nodes=['198948', '194947', '218370', '202949', '282455', '248143']
import math; v=[float(x) for x in nodes]; M=[[v[(i+j)%6]/sum(v) for j in range(6)] for i in range(6)]; exec("for _ in range(12):\n M=[[sum(M[i][k]*M[k][j] for k in range(6)) for j in range(6)] for i in range(6)]"); print(f"Steady_State_Eigenvector_Node4={M[0][4]:.15f} | Entropy={-sum(x*math.log2(x) for x in M[0]):.8f}_bits")
