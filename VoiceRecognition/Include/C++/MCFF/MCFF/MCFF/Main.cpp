#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <complex>

#define PI 3.14159265
#include "VoiceWindow.h"

using namespace std;

int main(int argc, char *argv[]){
	
	const unsigned int N = 20;

    const double x_1[N] = {0, 0.3, 0.6, 0.8, 1, 1, 0.9, 0.7, 0.5, 0.2, 0.2, 0.5, 0.7, 0.9, 1, 1, 0.8, 0.6, 0.3, 0};

    for(unsigned int k = 0; k < N; k++)
    {
        std::complex<double> sum(0.0,0.0);
        for(unsigned int j = 0; j < N; j++)
        {
            int integers = -2*j*k;
            std::complex<double> my_exponent(0.0, PI/N*(double)integers);
            sum += x_1[j] * std::exp(my_exponent);
        }
        std::cout << abs(sum)/N << std::endl;
    }
	
	system("PAUSE");
	return 0;
}

