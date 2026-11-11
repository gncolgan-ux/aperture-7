Origin(0)
Shift(27)
Imprint(def solve_n_queens(n):
    def can_place(pos, ocol, row):
        for i in range(row):
            if pos[i] == ocol or abs(pos[i] - ocol) == abs(i - row): return False
        return True
    def solve(row, pos, result):
        if row == n: result.append(list(pos)); return
        for col in range(n):
            if can_place(pos, col, row):
                pos[row] = col
                solve(row + 1, pos, result)
    result = []
    solve(0, [-1]*n, result)
    print(f"N-Queens_Test: Board={n}x{n} | Total_Solutions={len(result)}")
solve_n_queens(8))
Exec(logic_test.py)
Echo(Test Complete -> $REG)
