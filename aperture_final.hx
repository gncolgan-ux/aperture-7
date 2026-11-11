Def(OPEN : Loop(6 : Rotate(+1)Switch(@IDX - 1))Origin(0))
Def(ZERO : Call(OPEN)Origin(0)Calc(0)Loop(6 : Rotate(+1)Switch(@IDX - 1)Calc(0))Origin(0))
Def(P : Elevate(-1)Calc()Elevate(+1)Calc(@REG))
Def(PULL : Origin(0)Call(P)Loop(6 : Rotate(+1)Switch(@IDX - 1)Call(P))Origin(0))

Def(ADVECT : Loop(6 : Rotate(+1)Switch(@IDX - 1)Calc(@SELF - @C0 * @SELF * 0.001 + @SELF))Origin(0))
Def(STEP_PDE : Elevate(+1)Call(PULL)Call(ADVECT)Origin(0)Diffuse(1))

Def(LENS : Loop(6 : Rotate(+1)Switch(@IDX - 1)Calc()Calc(@REG - @C0)Calc(@REG * 10))Origin(0)Calc(0))
Def(DIODE : Loop(6 : Rotate(+1)Switch(@IDX - 1)Calc()IfL(0 : Calc(0)))Origin(0))
Def(U : Elevate(-1)Calc()Elevate(+1)Calc(@REG * 0.5 + @SELF))
Def(CASCADE : Loop(6 : Rotate(+1)Switch(@IDX - 1)Call(U))Origin(0)Calc(@E0 + @E1 + @E2 + @E3 + @E4 + @E5 * 0.166667))

Def(FB_NODE : Calc()Elevate(-24)Calc(@SELF + @REG * 0.25)Elevate(+24))
Def(REBUILD_BASE : Origin(0)Call(FB_NODE)Loop(6 : Rotate(+1)Switch(@IDX - 1)Call(FB_NODE))Origin(0)Elevate(-24)Diffuse(1))

Def(GEN : Loop(12 : Call(STEP_PDE))Elevate(+1)Call(PULL)Call(LENS)Elevate(+1)Call(PULL)Call(LENS)Elevate(+1)Call(PULL)Call(DIODE)Elevate(+1)Call(PULL)Loop(8 : Elevate(+1)Call(CASCADE))Call(REBUILD_BASE))

Elevate(-12)
Loop(24 : Call(ZERO)Elevate(+1))
Call(ZERO)

Elevate(-24)Origin(0)Calc(150)
Switch(0)Calc(80)Switch(1)Calc(500)
Switch(2)Calc(350)Switch(3)Calc(60)
Switch(4)Calc(40)Switch(5)Calc(200)

Loop(8 : Call(GEN))
Loop(12 : Call(STEP_PDE))

Origin(0)Collapse(+)Loop(6 : Rotate(+1)Switch(@IDX - 1)Collapse(+))Origin(0)
Save(latest.bin)
