#pragma once

#include <vector>
#include <complex>
#include <cmath>
#include <iostream>

# define M_PI 3.14159265358979323846  /* pi */

using namespace std;

void fft(vector<complex<float>>& in, vector<complex<float>>& out);
void ifft(vector<complex<float>>& in, vector<complex<float>>& out);

vector<complex<float>> create_test_case(int amount_of_complex);
void print_vector(vector<complex<float>>& in);

void fft_init();

