#ifndef VoiceWindow_H
#define VoiceWindow_H

void PreEmphasis(double *);
void FrameBlock(double *);	
void FilterBank(double *data, double *phase, int size);
void Cepstrum(double *);

#endif
