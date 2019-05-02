#pragma once


#include "fft.h"
#include <chrono>

using namespace std;


/*
int main() {
	
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

*/

/*
int main() {
	fft_init();

	//for (int i = 0; i < 8; i++)
		//test_case.push_back(i);
	vector<complex<float>> test_case = create_test_case(pow(2,3));

	auto start = std::chrono::high_resolution_clock::now();
	fft(test_case, test_case);

	auto elapsed = std::chrono::high_resolution_clock::now() - start;
	long long microseconds = std::chrono::duration_cast<std::chrono::microseconds>(elapsed).count();
	print_vector(test_case);

	ifft(test_case, test_case);
	print_vector(test_case);

	cout << endl << microseconds << endl;
	getchar();

}
*/