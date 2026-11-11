Def(OPEN : Loop(6 : Rotate(+1)Switch(@IDX - 1))Origin(0))
Def(P : Elevate(-1)Calc()Elevate(+1)Calc(@REG))
Def(PULL : Origin(0)Call(P)Loop(6 : Rotate(+1)Switch(@IDX - 1)Call(P))Origin(0))

Def(ADVECT : Loop(6 : Rotate(+1)Switch(@IDX - 1)Calc(@SELF - @C0 * @SELF * 0.005 + @SELF))Origin(0))
Def(STEP_PDE : Elevate(+1)Call(PULL)Call(ADVECT)Origin(0)Diffuse(1))
Def(SHOCK_GRAD : Loop(6 : Rotate(+1)Switch(@IDX - 1)Calc()Calc(@REG - @C0)Calc(@REG * 100))Origin(0)Calc(0))
Def(VORTEX : Loop(6 : Rotate(+1)Switch(@IDX - 1)Calc()IfL(0 : Calc(0)))Origin(0))

Elevate(0)Elevate(-6)
Loop(18 : Call(OPEN)Origin(0)Calc(0)Loop(6 : Rotate(+1)Switch(@IDX - 1)Calc(0))Elevate(+1))
Call(OPEN)

Elevate(0)Elevate(-6)Origin(0)Calc(45)
Switch(0)Calc(30)Switch(1)Calc(100)
Switch(2)Calc(80)Switch(3)Calc(25)
Switch(4)Calc(15)Switch(5)Calc(20)

Loop(12 : Call(STEP_PDE))

Elevate(7)Call(PULL)Call(SHOCK_GRAD)
Elevate(8)Call(PULL)Call(VORTEX)
Elevate(0)Origin(0)Collapse(+)Loop(6 : Rotate(+1)Collapse(+))Origin(0)
Save(latest.bin)
