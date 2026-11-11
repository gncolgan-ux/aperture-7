#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <cmath>
#include <sstream>
#include <iomanip>
#include <chrono>
using namespace std;
const double PI = acos(-1.0), TAU = 2.0 * PI;
struct Node { string role; double phase; string val; bool unlk; };

class VM {
public:
    map<int, vector<Node>> L; map<string, string> defs; int z=0, n=0, sc=0, dp=0; string rg="0"; bool ok=true;
    VM() { if(!load("lattice.bin")) ens(0); }
    static string tr(string s) {
        size_t a=s.find_first_not_of(" \t\r\n"), b=s.find_last_not_of(" \t\r\n");
        return a==string::npos ? "" : s.substr(a, b-a+1);
    }
    static double sd(string s) { try { return stod(tr(s)); } catch(...) { return 0; } }
    void ens(int l) {
        if(!L.count(l)) L[l]={{"CORE",TAU,"0",1},{"DB",PI/3,"0",0},{"OS",2*PI/3,"0",0},
            {"ALU",PI,"0",0},{"IO",4*PI/3,"0",0},{"LAN",5*PI/3,"0",0},{"AI",TAU,"0",0}};
    }
    static void ws(ofstream& o, string s) { uint32_t k=s.size(); o.write((char*)&k,4); o.write(s.data(),k); }
    static string rs(ifstream& i) { uint32_t k=0; i.read((char*)&k,4); string s(k,0); i.read(&s[0],k); return s; }
    void save(string p) {
        ofstream o(p, ios::binary|ios::trunc); uint32_t m=0x4858564D, c=L.size();
        o.write((char*)&m,4); o.write((char*)&z,4); o.write((char*)&n,4); o.write((char*)&sc,4); ws(o,rg); o.write((char*)&c,4);
        for(auto& [k,v]:L) {
            o.write((char*)&k,4);
            for(int i=0;i<7;++i) { ws(o,v[i].role); o.write((char*)&v[i].phase,8); ws(o,v[i].val); o.write((char*)&v[i].unlk,1); }
        }
    }
    bool load(string p) {
        ifstream in(p, ios::binary); if(!in) return 0; uint32_t m=0, c=0; in.read((char*)&m,4); if(m!=0x4858564D) return 0;
        in.read((char*)&z,4); in.read((char*)&n,4); in.read((char*)&sc,4); rg=rs(in); in.read((char*)&c,4); L.clear();
        for(uint32_t l=0;l<c;++l) {
            int k=0; in.read((char*)&k,4); vector<Node> v(7);
            for(int i=0;i<7;++i) { v[i].role=rs(in); in.read((char*)&v[i].phase,8); v[i].val=rs(in); in.read((char*)&v[i].unlk,1); }
            L[k]=v;
        }
        return 1;
    }
    string sub(string s) {
        ens(z); auto& r=L[z];
        auto rp=[&](string a, string b){ for(size_t p=0;(p=s.find(a,p))!=string::npos;p+=b.size()) s.replace(p,a.size(),b); };
        rp("@REG",rg); rp("@SELF",r[n].val); rp("@Z",to_string(z)); rp("@IDX",to_string(n?n:6)); rp("@C0",r[0].val);
        for(int i=0;i<6;++i) rp("@E"+to_string(i),r[i+1].val);
        rp("TAU",to_string(TAU)); rp("PI",to_string(PI)); return s;
    }
    double ev(string e) {
        e=tr(sub(e)); istringstream ss(e); double v=0, x=0; char op='+';
        while(ss >> x) {
            if(op=='+') v+=x; else if(op=='-') v-=x; else if(op=='*') v*=x; else if(op=='/'&&x!=0) v/=x;
            ss >> op;
        }
        return v;
    }
    static string fn(double v) {
        if(abs(v-round(v))<1e-6) return to_string((long long)round(v));
        ostringstream o; o<<fixed<<setprecision(2)<<v; return o.str();
    }
    static pair<string,string> sp(string s, char d) {
        for(size_t i=0,k=0;i<s.size();++i) {
            if(s[i]=='(') k++; else if(s[i]==')') k=k?k-1:0;
            else if(s[i]==d&&!k) return {tr(s.substr(0,i)),tr(s.substr(i+1))};
        }
        return {tr(s),""};
    }
    void run(string code) {
        if(dp>16) return; ok=true; size_t i=0, sz=code.size();
        while(i<sz && ok) {
            while(i<sz && isspace(code[i])) i++; if(i>=sz) break;
            size_t st=i; while(i<sz && (isalnum(code[i])||code[i]=='_')) i++;
            string c=code.substr(st,i-st); if(c.empty()||i>=sz||code[i]!='(') { i++; continue; }
            size_t as=++i; int k=1; while(i<sz && k>0) { if(code[i]=='(') k++; else if(code[i]==')') k--; i++; }
            string v=tr(code.substr(as,i-as-1)); ens(z); auto& r=L[z];
            if(c=="Origin") { n=0; r[0].unlk=1; }
            else if(c=="Shift") { int ix=(int)ev(sub(v))+1; if(ix>=1&&ix<=6){n=ix;r[n].unlk=0;} else ok=0; }
            else if(c=="Switch") { int k=(int)ev(v); if(k>=0&&k<6){n=k+1; r[n].unlk=true; sc+=15;} }
            else if(c=="Rotate") { int s=(int)ev(sub(v)); n=((n==0)?(s>=0?0:5):((n-1+s)%6+6)%6)+1; r[n].unlk=0; }
            else if(c=="Resonate") { if(abs(r[n].phase-ev(v))<=0.01){r[n].unlk=1;sc+=25;} else {sc=max(0,sc-15);ok=0;} }
            else if(c=="Set") { if(r[n].unlk) r[n].val=rg=sub(v); else ok=0; }
            else if(c=="Elevate") { string sv=sub(v); z=(!sv.empty()&&(sv[0]=='+'||sv[0]=='-'))?z+(int)ev(sv):(int)ev(sv); ens(z); }
            else if(c=="Math") { if(r[n].unlk){r[n].val=rg=fn(ev(v));sc+=10;} else ok=0; }
            else if(c=="Calc") { if(n>0&&!r[n].unlk){sc-=15;ok=0;return;} r[n].val=rg=fn(ev(v.empty()?r[n].val:v)); sc+=25; }
            else if(c=="Elevate") { string sv=sub(v); z=(!sv.empty()&&(sv[0]=='+'||sv[0]=='-'))?z+(int)ev(sv):(int)ev(sv); ens(z); }
            else if(c=="Collapse") { double sm=0; for(auto& [k,ly]:L) sm+=ev(ly[n].val); z=0; L[0][n].val=rg=fn(sm); sc+=50; }
            else if(c=="Def") { auto [nm,bd]=sp(v,':'); defs[nm]=bd; sc+=15; }
            else if(c=="Call") { if(defs.count(v)) run(defs[v]); else ok=0; }
            else if(c=="Loop") { auto [cs,b]=sp(v,':'); int cnt=(int)ev(cs); for(int j=0;j<cnt&&ok;++j) run(b); }
            else if(c=="IfG") { auto [th,b]=sp(v,':'); if(ev(rg)>ev(th)) run(b); }
            else if(c=="IfL") { auto [th,b]=sp(v,':'); if(ev(rg)<ev(th)) run(b); }
            else if(c=="Diffuse") { double c0=ev(r[0].val),e[6],sm=0; for(int j=0;j<6;++j) e[j]=ev(r[j+1].val); for(int j=0;j<6;++j){r[j+1].val=fn((e[(j+5)%6]+e[j]+e[(j+1)%6]+c0)/4.0);sm+=e[j];} r[0].val=rg=fn(sm/6.0); sc+=35; }
            else if(c=="Write") { if(!r[n].unlk){ok=0;continue;} auto [f,ct]=sp(v,':'); string fp="workspace/"+sub(f), bd=ct; ofstream o(fp,ios::trunc); o<<bd<<"\n"; o.close(); if(n) r[n].val="SAVED:"+sub(f); sc+=40; cout<<"[HX::WRITE] -> "<<fp<<"\n"; }
            else if(c=="Run") { string fp="workspace/"+sub(v); ifstream in(fp); if(!in){ok=0;continue;} ostringstream ss; ss<<in.rdbuf(); cout<<"[HX::RUN] <- "<<fp<<"\n"; dp++; run(tr(ss.str())); dp--; sc+=50; }
            else if(c=="Save") { string sp="workspace/"+(v.empty()?"snap.bin":sub(v)); save(sp); sc+=50; cout<<"[HX::SAVE] -> "<<sp<<"\n"; }
            else if(c=="Load") { string sp="workspace/"+sub(v); if(load(sp)){sc+=25;cout<<"[HX::LOAD] <- "<<sp<<"\n";} else ok=0; }
            else if(c=="Echo") { cout<<"[HX::Z"<<z<<"::"<<(n?"Edge_"+to_string(n-1):"Center_0")<<"] "<<(v=="*"?r[n].val:sub(v))<<"\n"; }
        }
    }
    void status() {
        cout<<"=== APERTURE BINARY VM (Score: "<<sc<<" | REG: "<<rg<<") ===\n";
        for(auto& [k,nd]:L) { cout<<"  [Z"<<k<<"] C0="<<nd[0].val; for(int i=1;i<=6;++i) cout<<" | E"<<(i-1)<<"="<<nd[i].val<<(nd[i].unlk?"*":""); cout<<"\n"; }
    }
};
int main(int c, char** v) {
    if(c<2) return 0; string a=v[1];
    if(a=="--reset") { remove("lattice.bin"); VM m; m.save("lattice.bin"); cout<<"[HX VM] Reset.\n"; return 0; }
    VM m; if(a=="--status") { m.status(); return 0; }
    auto t0=chrono::high_resolution_clock::now(); m.run(a); m.save("lattice.bin");
    cout<<"[COMMITTED | Score: "<<m.sc<<" | "<<fixed<<setprecision(1)<<chrono::duration<double,micro>(chrono::high_resolution_clock::now()-t0).count()<<" us]\n";
}
