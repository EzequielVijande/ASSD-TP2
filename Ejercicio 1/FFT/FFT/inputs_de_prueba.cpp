#include "fft.h"
#include <iostream>
#include <fstream>
#include <time.h>       /* time */

using namespace std;

void test_case_2_file(ofstream& file, vector<complex<float>>& prueba);


int main() {
	fft_init();
	ofstream myfile;
	myfile.open("inputs_prueba.txt");
	srand(time(NULL));

	for (int i = 0; i <= 5; i++) {
		for (int j = 0; j <= 1000; j++){
			myfile << "P" << endl;

			vector<complex<float>> prueba_in = create_test_case(pow(2, i));
			test_case_2_file(myfile, prueba_in);

			vector<complex<float>> prueba_out;
			fft(prueba_in, prueba_out);
			test_case_2_file(myfile, prueba_out);

			ifft(prueba_out, prueba_out);
			test_case_2_file(myfile, prueba_out);
		}
	}
	myfile.close();
	return 0;
}

void test_case_2_file(ofstream& file, vector<complex<float>>& prueba) {
	file << "[ complex";

	for (vector<complex<float>>::iterator it = prueba.begin(); it != prueba.end(); ++it) {
		if (it != prueba.begin())
			file << ", complex";

		file << *it;
	}
	file << " ]" << endl;
}


