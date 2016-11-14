#ifndef CONFIG_H
#define CONFIG_H

#define FrameSample 16000 //16KHZ (8KHZ)
#define PI 3.14159265
/*-------------------------------
			VoiceWindow
-------------------------------*/
#define PreEmp_Size 100
#define PreEmp_gain 0.95

#define FrameInterval 0.025
#define OverlapInterval 0.01
#define FFT_K 512
#define Frame_N (FrameSample*FrameInterval)
#define Frame_M (FrameSample*OverlapInterval)
#define Hamming_gain 0.46

#define FilterBank_Num 10
#define Lower_Freq 300
#define Upper_Freq 8000

double PreEmp_Output[FrameSample];
double FFT_Output[FrameSample];

#endif