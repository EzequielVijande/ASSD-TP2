#pragma once

#include <vector>
#include <complex>
#include <cmath>

# define M_PI 3.14159265358979323846  /* pi */

using namespace std;

void fft(vector<complex<float>>& in, vector<complex<float>>& out);
void ifft(vector<complex<float>>& in, vector<complex<float>>& out);

//vector<complex<float>> r_fft(complex<float>* x, int N, int s);
//vector<complex<float>> r_ifft(complex<float>* x, int N, int s);
