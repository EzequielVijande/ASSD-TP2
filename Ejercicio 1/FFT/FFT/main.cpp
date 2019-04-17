#pragma once

#include <vector>
#include <complex>
#include <iostream>
#include <cmath>

# define M_PI 3.14159265358979323846  /* pi */
using namespace std;

vector<int> bit_reversal(int log2_);
void fft(vector<complex<float>>& in, vector<complex<float>>& out);
void ifft(vector<complex<float>>& in, vector<complex<float>>& out);
void print_vector(vector<complex<float>>& in);
vector<complex<float>> r_fft(complex<float>* x, int N, int s);
vector<complex<float>> r_ifft(complex<float>* x, int N, int s);

int main() {
	//vector<complex<float>> in_seq{ complex<float>(5,1), complex<float>(3,0), complex<float>(6,0), complex<float>(8,32), complex<float>(10,0), complex<float>(11,0), 721, complex<float>(4,0)};
	vector<complex<float>> in_seq;
	for (int j = 0; j <= 7; j++)
		in_seq.push_back(complex<float>(j, 0));
	
	cout << "Vector original" << endl << endl;
	print_vector(in_seq);
	cout << endl <<"Vector ffteado" << endl;
	
	fft(in_seq, in_seq);
	
	print_vector(in_seq);
	
	cout << endl << "Vector Iffteado" << endl;
	ifft(in_seq, in_seq);

	print_vector(in_seq);
	getchar();
	
	return 0;
	
}


void fft(vector<complex<float>>& in, vector<complex<float>>& out) {
	vector<complex<float>> to_be_filled;
	to_be_filled = r_fft(&in[0], in.size() , 1);
	out = to_be_filled;
}

//https://en.wikipedia.org/wiki/Cooley%E2%80%93Tukey_FFT_algorithm#Data_reordering,_bit_reversal,_and_in-place_algorithms
/*
void fft(vector<complex<float>>& in, vector<complex<float>>& out) {
	int my_size = in.size();
	vector<int> running_sequence = bit_reversal(log2(my_size)+0.01);
	vector<complex<float>> to_be_filled(my_size, (0,0));

	for (int s = 0; s < (int)log2(my_size); s++) {
		int m = pow(2, s);
		complex<float> wm = std::exp(complex<float>(-2 * M_PI/m,0)*complex<float>(0,1));
		for (int k = 0; k < my_size; k=k+m) {
			complex<float> w = complex<float>(1,0);
			for (int j = 0; j < m / 2; j++) {
				complex<float> t = w * in.at(running_sequence[k+j+m/2]); 
				complex<float> u = in.at(running_sequence[k+j]);
				to_be_filled[k + j] = u + t;
				to_be_filled[k + j + m / 2] = u - t;
				w = w * wm;
			}
		}
	}
	out = to_be_filled;
}
*/

vector<complex<float>> r_fft(complex<float>* x, int N, int s) {
	vector<complex<float>> X(N, complex<float>(0, 0));
	if (N == 1) {
		X[0] = x[0];
	}
	else {
		vector<complex<float>> X1 = r_fft(x, N / 2, 2 * s);
		vector<complex<float>> X2 = r_fft(x + s, N / 2, 2 * s);
		for (int k = 0; k <= (N / 2 - 1); k++) {
			X[k] = X1[k] + complex<float>(cos(2 * M_PI*k / N), sin(-2 * M_PI*k / N))* X2[k];
			X[k + N / 2] = X1[k] - complex<float>(cos(2 * M_PI*k / N), sin(-2 * M_PI*k / N))* X2[k];
		}
	}
	return X;
}

void ifft(vector<complex<float>>& in, vector<complex<float>>& out) {
	vector<complex<float>> to_be_filled;
	to_be_filled = r_ifft(&in[0], in.size(), 1);
	for (vector<complex<float>>::iterator it = to_be_filled.begin(); it != to_be_filled.end(); ++it)
		(*it) = (*it) / (float)(to_be_filled.size());
	out = to_be_filled;
}

vector<complex<float>> r_ifft(complex<float>* x, int N, int s) {
	vector<complex<float>> X(N, complex<float>(0, 0));
	if (N == 1) {
		X[0] = x[0];
	}
	else {
		vector<complex<float>> X1 = r_ifft(x, N / 2, 2 * s);
		vector<complex<float>> X2 = r_ifft(x + s, N / 2, 2 * s);
		for (int k = 0; k <= (N / 2 - 1); k++) {
			X[k] = X1[k] + complex<float>(cos(2 * M_PI*k / N), sin(2 * M_PI*k / N))* X2[k];
			X[k + N / 2] = X1[k] - complex<float>(cos(2 * M_PI*k / N), sin(2 * M_PI*k / N))* X2[k];
		}
	}
	return X;
}
//https://en.wikipedia.org/wiki/Bit-reversal_permutation
vector<int> bit_reversal(int log2_) {
	static vector<vector<int>> sequences;
	static bool initialized = false;
	static int prev_max = 1;
	if (!initialized) {
		vector<int> init;
		init.push_back(0);
		sequences.push_back(init);
		init.push_back(1);
		sequences.push_back(init);
		initialized = true;
	}

	if (log2_ > prev_max) {
		for (int i = prev_max+1; i <= log2_; i++) {
			vector<int> prev = sequences.at(i-1);
			vector<int> next;

			for (vector<int>::iterator it = prev.begin(); it != prev.end(); ++it)
				next.push_back(*it*2);
			for (vector<int>::iterator it = prev.begin(); it != prev.end(); ++it)
				next.push_back(*it * 2 + 1);

			sequences.push_back(next);
		}
		prev_max = log2_;
	}
	for (vector<int>::iterator it = sequences.at(log2_).begin(); it != sequences.at(log2_).end(); ++it) 
		cout << *it << ", ";
	cout << endl;
	return sequences.at(log2_);
}


void print_vector(vector<complex<float>>& in) {
	for (vector<complex<float>>::iterator it = in.begin(); it != in.end(); ++it)
		cout << *it << ", ";
	cout << endl;
}