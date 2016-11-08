#ifndef CONFIG_H
#define CONFIG_H

#define FrameSample 16000 //16KHZ (8KHZ)
#define PI 3.14159265
/*-------------------------------
			VoiceWindow
-------------------------------*/
#define PreEmp_Size 100
#define PreEmp_gain 0.95

#define Frame_N 512
#define Hamming_gain 0.46

double PreEmp_Output[FrameSample];
double Hamming_Output[FrameSample];

#endif