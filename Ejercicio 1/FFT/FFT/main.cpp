#pragma once


#include "fft.h"
#include <iostream>
#include <chrono>

using namespace std;

void print_vector(vector<complex<float>>& in);
vector<complex<float>> create_test_case(int amount_of_complex);

int main() {
	
	vector<complex<float>> test_case;
	for (int i = 0; i < 8; i++) {
		test_case.push_back(i);
	}
	print_vector(test_case);
	cout << endl;
	fft(test_case, test_case);
	print_vector(test_case);
	cout << endl;
	ifft(test_case, test_case);
	print_vector(test_case);
	cout << endl;
	
	double p_n = 0;
	for (int n = 256; n <= 4096; n=n*2) {
		double test_time_n = 0;
		for (int i = 0; i<10000; i++) {
			vector<complex<float>> test_case =create_test_case(n);
			auto start = std::chrono::high_resolution_clock::now();
			fft(test_case, test_case);
			auto elapsed = std::chrono::high_resolution_clock::now() - start;
			long long microseconds = std::chrono::duration_cast<std::chrono::microseconds>(elapsed).count();
			test_time_n += microseconds/1000.0;		//miliseconds
		}
		p_n += test_time_n / n;
		
		cout << "t_" << n << "= " << test_time_n << endl;
		cout << "p_" << n << "=" <<(test_time_n / n) << endl;
	}
	cout << "suma de los p_n: " << "= " << p_n << endl;
	getchar();
	return 0;
}
vector<complex<float>> create_test_case(int amount_of_complex) {

	vector<complex<float>> test_case;
	double fMin =-100000, fMax = 100000;
	for (int i = 0; i < amount_of_complex; i++) {
		double f = (double)rand() / RAND_MAX;
		double f1 = fMin + f * (fMax - fMin);
		f = (double)rand() / RAND_MAX;
		double f2 = fMin + f * (fMax - fMin);
		test_case.push_back(complex<float>(f1,f2));
	}
	return test_case;
}


void print_vector(vector<complex<float>>& in) {
	for (vector<complex<float>>::iterator it = in.begin(); it != in.end(); ++it)
		cout << *it << ", ";
	cout << endl;
}


