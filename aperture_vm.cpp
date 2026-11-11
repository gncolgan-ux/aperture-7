#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <cmath>
#include <sstream>
#include <iomanip>
#include <chrono>

const double PI = std::acos(-1.0);
const double TAU = 2.0 * PI;

struct Node {
    std::string role;
    double phase;
    std::string val;
    bool unlocked;
};

class ApertureCPP {
public:
    std::map<int, std::vector<Node>> layers;
    int z_layer = 0;
    int active_node = 0; // 0 = Center_0, 1..6 = Edge_0..Edge_5
    std::string reg = "0";
    int score = 0;
    bool execution_active = true;

    ApertureCPP() { ensure_layer(0); }

    void ensure_layer(int z) {
        if (layers.find(z) == layers.end()) {
            layers[z] = {
                {"CORE_NEXUS",   TAU,            "0", true},
                {"SECTOR_0_DB",  1.0 * PI / 3.0, "0", false},
                {"SECTOR_1_OS",  2.0 * PI / 3.0, "0", false},
                {"SECTOR_2_ALU", 3.0 * PI / 3.0, "0", false},
                {"SECTOR_3_IO",  4.0 * PI / 3.0, "0", false},
                {"SECTOR_4_LAN", 5.0 * PI / 3.0, "0", false},
                {"SECTOR_5_AI",  6.0 * PI / 3.0, "0", false}
            };
        }
    }

    std::string node_name(int idx) {
        return idx == 0 ? "Center_0" : "Edge_" + std::to_string(idx - 1);
    }

    static std::string trim(const std::string& s) {
        size_t a = s.find_first_not_of(" \t\r\n");
        if (a == std::string::npos) return "";
        size_t b = s.find_last_not_of(" \t\r\n");
        return s.substr(a, b - a + 1);
    }

    std::string sub_vars(std::string s) {
        auto rep = [&](const std::string& from, const std::string& to) {
            size_t pos = 0;
            while ((pos = s.find(from, pos)) != std::string::npos) {
                s.replace(pos, from.length(), to);
                pos += to.length();
            }
        };
        rep("$REG", reg);
        rep("$Z", std::to_string(z_layer));
        rep("$IDX", std::to_string(active_node == 0 ? 6 : active_node));
        rep("TAU", std::to_string(TAU));
        rep("PI", std::to_string(PI));
        return s;
    }

    double eval_num(std::string expr) {
        expr = trim(sub_vars(expr));
        size_t mul = expr.find('*'), div = expr.find('/');
        if (mul != std::string::npos && div != std::string::npos) {
            double a = std::stod(trim(expr.substr(0, mul)));
            double b = std::stod(trim(expr.substr(mul + 1, div - mul - 1)));
            double c = std::stod(trim(expr.substr(div + 1)));
            return (a * b) / c;
        } else if (mul != std::string::npos) {
            return std::stod(trim(expr.substr(0, mul))) * std::stod(trim(expr.substr(mul + 1)));
        } else if (div != std::string::npos) {
            return std::stod(trim(expr.substr(0, div))) / std::stod(trim(expr.substr(div + 1)));
        }
        try { return std::stod(expr); } catch (...) { return 0.0; }
    }

    static std::string fmt_num(double v) {
        if (std::abs(v - std::round(v)) < 1e-6) return std::to_string((long long)std::round(v));
        std::ostringstream oss;
        oss << std::fixed << std::setprecision(2) << v;
        return oss.str();
    }

    static std::pair<std::string, std::string> split_top(const std::string& s, char delim) {
        int depth = 0;
        for (size_t i = 0; i < s.size(); ++i) {
            if (s[i] == '(') depth++;
            else if (s[i] == ')') depth = std::max(0, depth - 1);
            else if (s[i] == delim && depth == 0)
                return {trim(s.substr(0, i)), trim(s.substr(i + 1))};
        }
        return {trim(s), ""};
    }

    static std::vector<std::pair<std::string, std::string>> tokenize_balanced(const std::string& s) {
        std::vector<std::pair<std::string, std::string>> tokens;
        size_t i = 0, n = s.size();
        while (i < n) {
            while (i < n && std::isspace(s[i])) i++;
            if (i >= n) break;
            size_t start = i;
            while (i < n && (std::isalnum(s[i]) || s[i] == '_')) i++;
            std::string cmd = s.substr(start, i - start);
            if (cmd.empty() || i >= n || s[i] != '(') { i++; continue; }
            i++; // skip '('
            int depth = 1;
            size_t arg_start = i;
            while (i < n && depth > 0) {
                if (s[i] == '(') depth++;
                else if (s[i] == ')') depth--;
                i++;
            }
            tokens.push_back({cmd, trim(s.substr(arg_start, i - arg_start - 1))});
        }
        return tokens;
    }

    void execute_wave(const std::string& code) {
        execution_active = true;
        auto tokens = tokenize_balanced(code);
        for (auto& [cmd, val] : tokens) {
            if (!execution_active) break;
            ensure_layer(z_layer);
            auto& rosette = layers[z_layer];

            if (cmd == "Origin") {
                active_node = 0;
                rosette[0].unlocked = true;
                std::cout << "  [Origin] -> Z" << z_layer << "::Center_0\n";
            } else if (cmd == "Shift") {
                int idx = std::stoi(val) + 1;
                if (idx >= 1 && idx <= 6) {
                    active_node = idx;
                    rosette[active_node].unlocked = false;
                    std::cout << "  [Shift] -> Z" << z_layer << "::" << node_name(active_node)
                              << " (" << rosette[active_node].role << ")\n";
                } else execution_active = false;
            } else if (cmd == "Rotate") {
                int step = std::stoi(val);
                int cur = (active_node == 0) ? (step >= 0 ? 0 : 5) : ((active_node - 1 + step) % 6 + 6) % 6;
                active_node = cur + 1;
                rosette[active_node].unlocked = false;
            } else if (cmd == "Emit") {
                double p = eval_num(val);
                rosette[active_node].phase = p;
                rosette[active_node].unlocked = true;
                std::cout << "  [Emit] Z" << z_layer << "::" << node_name(active_node) << " retuned -> " << p << " rad\n";
            } else if (cmd == "Resonate") {
                double target = eval_num(val);
                double actual = rosette[active_node].phase;
                if (std::abs(actual - target) <= 0.005) {
                    rosette[active_node].unlocked = true;
                    score += 25;
                    std::cout << "  [Resonate] SHIELD BREACHED at Z" << z_layer << "::" << node_name(active_node)
                              << " (" << std::fixed << std::setprecision(4) << target << " rad) [+25 PTS]\n";
                } else {
                    score = std::max(0, score - 15);
                    std::cout << "  [Resonate] SHIELD DEFLECTED at Z" << z_layer << "::" << node_name(active_node)
                              << " (Expected " << actual << ", got " << target << ") [-15 PTS]\n";
                    execution_active = false;
                }
            } else if (cmd == "Set" || cmd == "Imprint" || cmd == "Read") {
                if (!rosette[active_node].unlocked) { execution_active = false; continue; }
                rosette[active_node].val = reg = sub_vars(val);
                std::cout << "  [" << cmd << "] Z" << z_layer << "::" << node_name(active_node) << " = " << reg << "\n";
            } else if (cmd == "Elevate") {
                if (!val.empty() && (val[0] == '+' || val[0] == '-')) z_layer += std::stoi(val);
                else z_layer = (int)eval_num(val);
                ensure_layer(z_layer);
                std::cout << "  [Elevate] -> 3D Floor Z" << z_layer << "::" << node_name(active_node) << "\n";
            } else if (cmd == "Math") {
                if (!rosette[active_node].unlocked) { execution_active = false; continue; }
                double res = eval_num(val);
                rosette[active_node].val = reg = fmt_num(res);
                score += 10;
                std::cout << "  [Math] " << sub_vars(val) << " => " << reg << " [+10 PTS]\n";
            } else if (cmd == "While") {
                auto [cond, body] = split_top(val, ':');
                auto [lhs, rhs] = split_top(cond, '<');
                int safety = 0;
                while (execution_active && safety++ < 250) {
                    if (!(eval_num(lhs) < eval_num(rhs))) break;
                    execute_wave(body);
                }
            } else if (cmd == "Loop") {
                auto [cnt_s, body] = split_top(val, ':');
                int cnt = (int)eval_num(cnt_s);
                for (int i = 0; i < cnt && execution_active; ++i) execute_wave(body);
            } else if (cmd == "Collapse") {
                double sum = 0;
                int count = 0;
                for (auto& [z, lyr] : layers) {
                    if (lyr[active_node].val != "0" && !lyr[active_node].val.empty()) {
                        sum += std::stod(lyr[active_node].val);
                        count++;
                    }
                }
                z_layer = 0;
                layers[0][active_node].val = reg = fmt_num(sum);
                score += 50 * count;
                std::cout << "  [Collapse:+] " << count << " 3D floors collapsed -> Z0::" << node_name(active_node)
                          << " = " << reg << " (Score: " << score << ")\n";
            } else if (cmd == "Diffuse") {
                double c0 = std::stod(rosette[0].val);
                double e[6];
                for (int i = 0; i < 6; ++i) e[i] = std::stod(rosette[i + 1].val);
                double sum = 0;
                for (int i = 0; i < 6; ++i) {
                    double coupled = (e[(i + 5) % 6] + e[i] + e[(i + 1) % 6] + c0) / 4.0;
                    rosette[i + 1].val = fmt_num(coupled);
                    sum += e[i];
                }
                rosette[0].val = reg = fmt_num(sum / 6.0);
                score += (int)std::abs(sum / 6.0);
                std::cout << "  [Diffuse] Wave Equilibrium -> Center_0=" << reg << " (Score: " << score << ")\n";
            } else if (cmd == "Shield") {
                auto [try_w, catch_w] = split_top(val, ':');
                int sv_n = active_node, sv_z = z_layer;
                execute_wave(try_w);
                if (!execution_active) {
                    std::cout << "  [Shield] Absorbed phase rebound -> Rerouting...\n";
                    execution_active = true;
                    active_node = sv_n; z_layer = sv_z;
                    if (!catch_w.empty()) execute_wave(catch_w);
                }
            } else if (cmd == "Exec") {
                if (!rosette[active_node].unlocked) { execution_active = false; continue; }
                rosette[active_node].val = reg = "CPP_EXEC[" + val + "]";
                score += 30;
                std::cout << "  [Exec:Z" << z_layer << "::" << node_name(active_node) << "] " << reg << " [+30 PTS]\n";
            } else if (cmd == "Echo") {
                std::string out = (val == "*") ? rosette[active_node].val : sub_vars(val);
                std::cout << "  ==> [Echo] Z" << z_layer << "::" << node_name(active_node) << " :: " << out << "\n";
            }
        }
    }
};

void run_test(const std::string& label, const std::string& wave) {
    std::cout << "\n======================================================\n";
    std::cout << "WAVE TEST: " << label << "\n";
    std::cout << "STREAM   : " << wave << "\n";
    std::cout << "------------------------------------------------------\n";
    ApertureCPP vm;
    auto t0 = std::chrono::high_resolution_clock::now();
    vm.execute_wave(wave);
    auto t1 = std::chrono::high_resolution_clock::now();
    double us = std::chrono::duration<double, std::micro>(t1 - t0).count();
    std::cout << "------------------------------------------------------\n";
    std::cout << "FINAL SCORE: " << vm.score << " PTS | EXECUTION TIME: " << std::fixed << std::setprecision(1) << us << " microseconds\n";
}

int main() {
    run_test("1. hello.hx", "Emit(3.1415)Shift(2)Resonate(3.1415)Echo(Hello_Aura)");
    run_test("2. intruder.hx (Unauthorized Phase Lock)", "Shift(2)Resonate(1.9999)Echo(*)");
    run_test("3. core_complete.hx (3D Tower While + Collapse)", "Elevate(0)Origin(0)Set(2)While($REG < 64 : Elevate(+1)Math($REG * 4))Collapse(+)Echo(TURING_CORE_3D_TOTAL:$REG)");
    run_test("4. gold_master.hx (Shield Recovery + 3D Tower)", "Shield(Shift(2)Resonate(9.9999)Set(Fail) : Origin(0)Echo(SHIELD_RECOVERY_ACTIVE))Elevate(0)Origin(0)Read(5)While($REG < 100 : Elevate(+1)Math($REG * 3))Collapse(+)Echo(GOLD_MASTER_100_PERCENT:$REG)");
    run_test("5. endgame.hx (Full 6-Edge Rotation + Laplacian Diffuse)", "Elevate(0)Origin(0)Set(60)Loop(6:Rotate(+1)Resonate($IDX * PI / 3)Math($IDX * 10))Origin(0)Diffuse(1)Shift(0)Resonate(PI/3)Exec(Mount_H3)Shift(4)Resonate(5*PI/3)Exec(127.0.0.1)Shift(5)Resonate(TAU)Exec(Status)Origin(0)Echo(ENDGAME_KERNEL_ONLINE:$REG)");
    return 0;
}
