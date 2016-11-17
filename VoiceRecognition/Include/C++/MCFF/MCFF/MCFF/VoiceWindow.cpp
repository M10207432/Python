#include "VoiceWindow.h"
#include "Config.h"
#include <math.h>
#include <complex>

using namespace std;

/*====================
				Signal pass through 
					High Pass Filter
s2(n) = s(n) - PreEmp_gain*s(n-1) 
(0.8<PreEmp_gain<0.9)
====================*/
void PreEmphasis(double *data){

	for(int i=1; i<FrameSample; i++){
		*(PreEmp_Output+i)=*(data+i)-(*(data+i-1))*PreEmp_gain;
	}

}

/*=============================
			<Frame Block with Hamming Block & FFT>
		For getting N point as one frame
		There would have M points overlay
(Signal Sampling freq is 8KHZ~16KHZ)
(N 256 or 512)
=============================*/
void FrameBlock(double *data, int frame_id, int frame_end){
	
	complex<double> DFT_Val[Frame_N];	// complex(Real,Img)
	double phase[Frame_N];
	double Energy[Frame_N];
	double Mel[FilterBank_Num];
	double Hamming_Wid=0;
	int size=(frame_end-frame_id);

	//Avoid over Frame Size
	if((frame_end-frame_id)>Frame_N){
		printf("The Frame size is wrong\n");
		return ;
	}

	//Evaluate DFT for each Window-----------------------------Step1 (Evaluate DFT for each frame)
	for(int k=0; k<size; k++){
		complex<double> sum(0.0,0.0);	// complex(Real,Img)

		//Evaluate for each FFT (0~N-1)
		for(int n=0; n<size; n++){

			Hamming_Wid=(1-Hamming_gain)-Hamming_gain*cos((2*PI*n)/(Frame_N-1));
			complex<double> exp_pow(0.0,( -2*PI*k*n)/Frame_N);		// complex(Real,Img)
				
			sum=(data[n+frame_id])*Hamming_Wid*exp(exp_pow);		
		}

		Energy[k]=(abs(sum)*abs(sum));
		DFT_Val[k]=sum;
		phase[k]=arg(sum);
		//DFT_Energy[k+frame_id]=(abs(sum)*abs(sum))/Frame_N;
	}

	//-------------------------------------------------------------Step2 (Bank Filter)
	FilterBank( &Mel[0], &Energy[0], size);

	//-------------------------------------------------------------Step2 (Bank Filter) Update MCFF[]
	Cepstrum(&Mel[0]);

}

void FilterBank( double *Mel, double *Energy, int size){
	
	double F_pre,F_m,F_post;
	double Mel_para;
	double mel_lower_freq=1125*log(1+Lower_Freq/700);
	double mel_upper_freq=1125*log(1+Upper_Freq/700);
	double mel_f[FilterBank_Num+2];
	double BIN[FilterBank_Num+2];

	//Transfer to Mel Frequence
	mel_f[0]=0;
	for(int i=1; i<FilterBank_Num+2; i++){
		mel_f[i]=mel_lower_freq+((mel_upper_freq-mel_lower_freq)/(FilterBank_Num+1))*(i-1);
		mel_f[i]=700*(exp(mel_f[i]/1125)-1);

		//FFT BIN [f(i) = floor((nfft+1)*h(i)/samplerate)]
		BIN[i]=floor(Frame_N*mel_f[i]/FrameSample); 
	}

	//Get Filter Bank Parameter
	for(int i=1; i<FilterBank_Num+1; i++){
		
		//Find the filter id
		F_pre=BIN[i-1];
		F_m=BIN[i];
		F_post=BIN[i+1];

		//Energy pass through filter bank
		for(int k=0; k<size; k++){

			//Get the parameter
			if(k<F_pre){
				Mel_para=0;
			}else if(k >= F_pre && k<F_m){
				Mel_para=(k-F_pre)/(F_m-F_pre);
			}else if(k >= F_m && k<F_post){
				Mel_para=(F_post-k)/(F_post-F_m);
			}else if(k >= F_post){
				Mel_para=0;
			}

			//Energy Evaluate
			Mel[i-1]=Energy[k]*Mel_para;
		}
	}
}

void Cepstrum(double *data){

	double Cn;

	//Discrete Cosine Transform
	for(int i=0; i<Mel_L; i++){
		Cn=0;
		for(int j=0; j<FilterBank_Num; j++){
			Cn=Cn+(log(data[j]))*cos(i*(j-0.5)*PI/FilterBank_Num);
		}
		MCFF[i]=Cn;
	}
}