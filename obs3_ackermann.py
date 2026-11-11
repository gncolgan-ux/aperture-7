nodes=['198948', '194947', '218370', '202949', '282455', '248143']
import sys; sys.set_int_max_str_digits(50000); v=[int(x) for x in nodes]; ack=(1<<(1<<(v[4]%17)))-3; print(f"3.ACKERMANN_A(4,2)_TOWER: Exact_Decimal_Digits={len(str(ack))} | Leading12={str(ack)[:12]} | Trailing12={str(ack)[-12:]}")
