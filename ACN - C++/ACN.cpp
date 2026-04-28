#include <bits/stdc++.h>
using namespace std;
typedef long long ll;


struct ar1{
    ll s;
    vector<double> v;
    ar1(ll n=0, double x = 0, double r=0){
        s = n;
        v = vector<double>(n, x);
        if(r>0) for(auto &i : v) i+=r*(double)(rand())/(double)(RAND_MAX);
    }
    ar1(vector<double> x){
        s=x.size();
        v=x;
    }
    ar1(ar1 x, ar1 y){
        s=x.s;
        v=x.v;
        for(auto i : y.v){s++;v.push_back(i);}
    }
    ar1(ar1 x, ll n){
        s=x.s-n;
        v=vector<double>(0);
        for(ll i = n; i < x.v.size(); i++)v.push_back(x.v[i]);
    }
    void set(vector<double> x){
        v = x;
    }
    ar1 deepcopy(){
        ar1 y(s);
        for(ll i = 0; i < s; i++){
            y.v[i]=v[i];
        }
        return y;
    }
    void swp(ar1 &y){
        swap(s,y.s);
        swap(v,y.v);
    }
    void print(){
        for(ll i = 0; i < s; i++){
            cout << v[i] << " ";
        }
        cout << endl;
    }
    ar1 app(function<double(double)> f){
        ar1 y(s);
        for(ll i = 0; i < s; i++){
            y.v[i] = f(v[i]);
        }
        return y;
    }
    ar1 operator+(ar1 x){
        ar1 y(s);
        for(ll i = 0; i < s; i++){
            y.v[i]=v[i]+x.v[i];
        }
        return y;
    }
    void operator+=(ar1 x){
        for(ll i = 0; i < s; i++){
            v[i]+=x.v[i];
        }
    }
    ar1 operator*(double x){
        ar1 y(s);
        for(ll i = 0; i < s; i++){
            y.v[i]=v[i]*x;
        }
        return y;
    }
    void operator*=(double x){
        for(ll i = 0; i < s; i++){
            v[i]*=x;
        }
    }
    ar1 mult(ar1 x){
        ar1 y(s);
        for(ll i = 0; i < s; i++){
            y.v[i] = v[i]*x.v[i];
        }
        return y;
    }
};

struct ar2{
    vector<ll> s;
    vector<ar1> v;
    ar2(vector<ll> n, double x = 0, double r = 0){
        s = n;
        v = vector<ar1>(n[0], ar1(n[1],x,r));
    }
    void set(vector<vector<double>> x){
        for(ll i = 0; i < s[0]; i++){
            v[i].set(x[i]);
        }
    }
    ar2 deepcopy(){
        ar2 y(s);
        for(ll i = 0; i < s[0]; i++){
            y.v[i] = v[i].deepcopy();
        }
        return y;
    }
    void print(){
        for(ll i = 0; i < s[0]; i++){
            v[i].print();
        }
        cout << endl;
    }
    ar2 operator+(ar2 x){
        ar2 y(s);
        for(ll i = 0; i < s[0]; i++){
            y.v[i] = v[i] + x.v[i];
        }
        return y;
    }
    void operator+=(ar2 x){
        for(ll i = 0; i < s[0]; i++){
            v[i] += x.v[i];
        }
    }
    ar1 operator*(ar1 x){
        ar1 y(s[1]);
        for(ll i = 0; i < s[0]; i++){
            y+=(v[i]*x.v[i]);
        }
        return y;
    }
    ar2 operator*(double x){
        ar2 y(s);
        for(ll i = 0; i < s[0]; i++){
            y.v[i]=v[i]*x;
        }
        return y;
    }
    void operator*=(double x){
        for(ll i = 0; i < s[0]; i++){
            v[i] *= x;
        }
    }
    ar2 transpose(){
        ar2 y({s[1],s[0]});
        for(ll i = 0; i < s[0]; i++){
            for(ll j = 0; j < s[1]; j++){
                y.v[j].v[i] = v[i].v[j];
            }
        }
        return y;
    }
    ar2 mult(ar1 x){
        ar2 y(s);
        for(ll i = 0; i < s[0]; i++){
            y.v[i] = v[i]*x.v[i];
        }
        return y;
    }
};

struct nn{
    ll d;
    vector<ll> s;
    vector<ar2>w;
    vector<ar1>b;
    vector<ar1>pre;
    vector<ar1>post;
    ar1 ingr;
    nn(vector<ll> n, double x = 0,double r=0){
        d = n.size()-1;
        s = n;
        for(ll i = 0; i < d; i++){
            w.push_back(ar2({s[i],s[i+1]},x,r));
            b.push_back(ar1(s[i+1],x,r));
            pre.push_back(ar1(s[i]));
            post.push_back(ar1(s[i]));
        }
        pre.push_back(ar1(s[d]));
        post.push_back(ar1(s[d]));
        ingr=ar1(n[0]);
    }
    void print(){
        cout << "weights:" << endl;
        for(ll i = 0; i < d; i++){
            w[i].print();
        }
        cout << "biases:" << endl;
        for(ll i = 0; i < d; i++){
            b[i].print();
        }
    }
    void operator+=(nn x){
        for(ll i = 0; i < d; i++){
            w[i] += x.w[i];
            b[i] += x.b[i];
        }
    }
    nn operator*(double x){
        nn y(s);
        for(ll i = 0; i < d; i++){
            y.w[i] = w[i]*x;
            y.b[i] = b[i]*x;
        }
        return y;
    }
    void operator*=(double x){
        for(ll i = 0; i < d; i++){
            w[i] *= x;
            b[i] *= x;
        }
    }
    ar1 app(ar1 in, function<double(double)> f){
        post[0]=in.deepcopy();
        for(ll i = 0; i < d-1; i++){
            pre[i+1]=w[i]*post[i]+b[i];
            post[i+1]=pre[i+1].app(f);
        }
        pre[d]=w[d-1]*post[d-1];
        pre[d] += b[d-1];
        return pre[d];
    }
    nn diff(ar1 out, function<double(double)> df){
        nn y(s);
        y.b[d-1]=out.deepcopy();
        for(ll i = d-1; i > 0; i--){
            y.w[i]=ar2({s[i],s[i+1]},1).mult(post[i]).transpose().mult(y.b[i]).transpose();
            y.b[i-1]=(w[i].transpose()*y.b[i]).mult(pre[i].app(df));
        }
        y.w[0]=ar2({s[0],s[1]},1).mult(post[0]).transpose().mult(y.b[0]).transpose();
        ingr=(w[0].transpose()*y.b[0]);
        return y;
    }
};

double pi = acos(-1);

double dot(vector<double>a,vector<double>b){
    return a[0]*b[0]+a[1]*b[1];
}

vector<double> dir(double a){
    return {cos(a),sin(a)};
}

double 
    shipfrontdrag=0.01,
    shipsidedrag=0.5,
    rudderdrag=0.2,
    shiplength=1,
    saildrag=0.1,
    shipturndrag=0.2,
    windstrength=1,
    shipmomentinertia=1,
    sailmaxangle=pi,
    ruddermaxangle=pi/6;

double reward(vector<double> &state){
    double x = sqrt(state[1]*state[1]+state[2]*state[2]);
    return((x<=2)*100000-x);
}

void sim(vector<double> &state,ar1 action){//reward, posx, posy, velx, vely, angle, anglevel, iter //sail, rudder
    
    double
        bfv=dot(dir(state[5]),{state[3],state[4]}),
        brv=dot(dir(state[5]-pi/2),{state[3],state[4]}),
        rrv=dot(dir(state[5]-pi/2+action.v[1]),{state[3]+sin(state[5])*shiplength*state[6],state[4]-cos(state[5])*shiplength*state[6]}),
        sfv=dot(dir(state[5]+action.v[0]),{windstrength-state[3],-state[4]});



    state={//mangler at resette til nyt tilfældigt checkpoint når man rammer det tidligere.
        reward(state),
        state[1]+state[3],
        state[2]+state[4],
        state[3]-bfv*shipfrontdrag*cos(state[5])-brv*shipsidedrag*sin(state[5])-rrv*rudderdrag*sin(state[5]+action.v[1])+sfv*saildrag*cos(state[5]+action.v[0]),
        state[4]-bfv*shipfrontdrag*sin(state[5])+brv*shipsidedrag*cos(state[5])-rrv*rudderdrag*sin(state[5]+action.v[1])+sfv*saildrag*sin(state[5]+action.v[0]),
        state[5]+state[6]-((ll)(180*state[5]/pi)/360)*2*pi,
        state[6]-rrv*cos(action.v[1])/shipmomentinertia-state[6]*shipturndrag,
        state[7]+1,
        state[8]
    };

}

ar1 sense(vector<double> state){//mangler
    return ar1((vector<double>){state[1],state[2]});
}

auto act = [](double x){return (x>10?x:(x<-10?0:log(1+exp(x))));};
auto dact = [](double x){return (x>10?1:(x<-10?0:1/(1+exp(-x))));};

auto actout = [](double x){return tanh(x);};
auto dactout = [](double x){return 1-tanh(x)*tanh(x);};

double b = 0.9;
double g = 0.001;

double rewardDecay = 0.99;
double heat = 0.2;

vector<ll>actorShape={2,2};
nn actor(actorShape,-0.5,1);
nn actorGrad(actorShape);

vector<ll>criticShape={4,4,1};
nn critic(criticShape,-0.5,1);
nn criticGrad(criticShape);

ll innum=2;
ll outnum=2;

ll memsize=1000;
vector<array<ar1,2>>mem(memsize,{ar1(innum),ar1(outnum)});
vector<double>memrew(memsize,0);
ll memoffs=0;

ll batchsize=100;

random_device rd;
mt19937 gen(rd());
uniform_int_distribution<> distrib(0, memsize-1);


int main(){
    /*actor.b[0].v[0]=0;
    actor.w[0].v[0].v[0]=-1;
    critic.b[0].v={0,0};
    critic.b[0].v={0};
    critic.w[0].v[0].v={1,-1};
    critic.w[0].v[1].v={1,-1};
    critic.w[1].v[0].v[0]=-1;
    critic.w[1].v[1].v[0]=-1;*/
    vector<double>state={0,-100,0,0,0,0,0,0,0};//var
    ar1 action(outnum),prevaction(outnum);
    ar1 input(innum),previnput(innum);
    while(true){
        previnput.swp(input);
        prevaction.swp(action);
        input=sense(state);
        action=(actor.app(sense(state),act)+ar1(outnum, -0.5*heat, heat)).app(actout);
        sim(state,action);
        mem[memoffs]={previnput,prevaction};
        memrew[memoffs]=state[0]+(critic.app(ar1(input,action),act).v[0])*rewardDecay;
        memoffs++;
        memoffs%=memsize;

        if(((ll)state[7])%1==0){//var
            cout << "NEW " << endl;
            cout << "ACTOR" << endl;
            actor.print();
            cout << "CRITIC" << endl;
            critic.print();
            //cout << "STATE " << state[1] << " " << state[2] << " " << action.v[0] << " " << action.v[1] << " " << memrew[memoffs]-state[0] << " " << iter << endl;//var
        }
        

        actorGrad*=b;
        criticGrad*=b;
        for(ll i = 0; i < batchsize; i++){
            ll ind = distrib(gen);
            double des = memrew[ind];
            double res = (critic.app(ar1(mem[ind][0],mem[ind][1]),act)).v[0];
            //cout << "input " << mem[ind][0].v[0] << " output " << mem[ind][1].v[0] << " des " << des << " res " << res << endl;
            criticGrad+=critic.diff(ar1(1,des-res),dact)*(g*(1-b)/batchsize);
            ar1 trainingaction=actor.app(mem[ind][0],act);
            critic.app(ar1(mem[ind][0],trainingaction.app(actout)),act);

            critic.diff(ar1(1,1),dact);
            actorGrad+=actor.diff(ar1(critic.ingr,innum).mult(trainingaction.app(dactout)),dact)*(g*(1-b)/batchsize);
        }
        actor+=actorGrad;
        critic+=criticGrad;
        //usleep(50000);//var
    }




}