#include<stdlib.h>
#include<armadillo>
#include<fstream>
#include<cmath>
#include<map>
#include<random>
#include"spins.h"
using namespace std;
using namespace arma;

int Spins::periodic(int x)
{
    if(x == -1)
    {
        return L-1;
    }
    else if(x == L)
    {
        return 0;
    }
    else
    {
        return x;
    }
}

void Spins::init(int L, double T, double J, mt19937_64 &engine)
{
    this->L = L;
    this->T = T;
    this->J = J;

    rand_spin  = uniform_int_distribution<int>(0,1);
    rand_coord = uniform_int_distribution<int>(0,L-1);

    acceptAmp.insert( pair<double,double>(-8,exp(-1/T*(-8))) );
    acceptAmp.insert( pair<double,double>(-4,exp(-1/T*(-4))) );
    acceptAmp.insert( pair<double,double>(0,1));
    acceptAmp.insert( pair<double,double>(4,exp(-1/T*(4))) );
    acceptAmp.insert( pair<double,double>(8,exp(-1/T*(8))) );
}

Spins::Spins(){};

Spins::Spins(int L, double T, double J, mt19937_64 &engine)
{
    init(L, T, J, engine);
    ensemble = zeros<Mat<int>>(L,L);
    for(int i=0; i<L; i++)
    {
        for(int j=0; j<L; j++)
        {
            ensemble(i,j) = 2*rand_spin(engine) - 1;
        }
    }
    calcEnergy();
    calcMagnetization();
}

Spins::Spins(Mat<int> ensemble, int L, double T, double J, mt19937_64 &engine)
{
    init(L, T, J, engine);
    this->ensemble = ensemble;
    calcEnergy();
    calcMagnetization();
}

void Spins::calcEnergy()
{
    energy = 0;
    for(int i=0; i<L-1; i++)
    {
        energy -= ensemble(L-1,i)*(ensemble(L-1,i+1) + ensemble(0,i));
        energy -= ensemble(i,L-1)*(ensemble(i+1,L-1) + ensemble(i,0));
        for(int j=0; j<L-1; j++)
        {
            energy -= ensemble(i,j)*(ensemble(i+1,j) + ensemble(i,j+1));
        }
    }
    energy -= ensemble(L-1,L-1)*(ensemble(L-1,0) + ensemble(0,L-1));
}

void Spins::calcMagnetization()
{
    magnetization = 0;
    for(int i=0; i<L; i++)
    {
        for(int j=0; j<L; j++)
        {
            magnetization += ensemble(i,j);
        }
    }
}

void Spins::print()
{
    cout << ensemble << endl;
}

void Spins::tryflip(double &aA, mt19937_64 &engine)
{
    x = rand_coord(engine);
    y = rand_coord(engine);
    deltaE = 2*ensemble(x,y)*(
               ensemble(x,periodic(y+1)) + ensemble(x,periodic(y-1)) +
               ensemble(periodic(x+1),y) + ensemble(periodic(x-1),y));
    deltaM = -2*ensemble(x,y);
    aA = acceptAmp.find(deltaE)->second; //Returns the amplitude associated
                                         //with the change in energy
}
void Spins::flip()
{
    ensemble(x,y) *= -1;
}
