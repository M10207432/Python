#include "MachineLearn.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <fstream>
#include <iostream>
#include <time.h>
using namespace std;

/*======================
	Global Variable
======================*/

double input[SetNum][InputNum];			//last one for end
double output[SetNum][OutputNum];	//last one for end

double result[OutputNum];				//For calculate the result
double outputErr[OutputNum];
double hiddenErr[HiddenNum];

double th_output[OutputNum];
double IH_weight[InputNum][HiddenNum];
double HO_weight[HiddenNum][OutputNum];

#if default_setting
int default_idx=0;
double default_weight[]={0.2,-0.3,0.4,0.1,-0.5,0.2,-0.3,-0.2,-0.4,0.2,0.1};
#endif
Node* HEAD_Hidden;

char* path="../../IO.txt";
/*======================
						Function
======================*/


void AssignIO(char * path){
	ifstream  file;
	srand(time(NULL));

	//Open file & Arrange structure
	file.open(path,ios::in);

	for(int set_id=0; set_id<SetNum;set_id++){
		for(int i=0; i<InputNum; i++){
			file>>input[set_id][i];
		}
		for(int j=0; j<OutputNum; j++){
			file>>output[set_id][j];
		}
	}

	//Input to Hidden Arrange [rand() from -1~1]
	for(int i=0; i<InputNum; i++){
		for(int j=0; j<HiddenNum; j++){
#if default_setting
			IH_weight[i][j]=default_weight[default_idx];
			default_idx++;
#else
				IH_weight[i][j]=(double)(rand()%(RandRng*2))/RandRng-1;	
#endif
		}
	}

	//Hidden to Output Arrange [rand() from -1~1]
	for(int i=0; i<HiddenNum; i++){
		for(int j=0; j<OutputNum; j++){
#if default_setting
			HO_weight[i][j]=default_weight[default_idx];
			default_idx++;
#else
			HO_weight[i][j]=(double)(rand()%(RandRng*2))/RandRng-1;
#endif
			
		}
	}

	//Output threshold [rand() from -1~1]
	for(int i=0; i<OutputNum; i++){
#if default_setting
		th_output[i]=default_weight[10];
		default_idx++;
#else
		th_output[i]=(double)(rand()%(RandRng*2))/RandRng-1;
#endif
		
	}

}


void AssignHiddenNode(){
	HEAD_Hidden=(Node *)malloc(sizeof(Node));
	Node* tmp=HEAD_Hidden;
	
	//Assign Hidden layer link list
	tmp->next=NULL;
	for(int i=0; i<HiddenNum; i++){
		Node* n=(Node *)malloc(sizeof(Node));

		n->id=i;
		n->error=0;
#if default_setting
		static int id=8;
		n->threshold=default_weight[id++];
#else
	n->threshold=(double)(rand()%(RandRng*2))/RandRng-1;
#endif
		
		tmp->next=n;
		tmp=n;
	}
	tmp->next=NULL;
}


void MatrixEvaluate(double  *input, Node *hiddenNode){
	/*----------------------------------
			Evaluate Ouput &
			Assign value 
	----------------------------------*/

	Node* hidden=hiddenNode->next;
	for(int hi_idx=0; (hi_idx<HiddenNum && hidden!=NULL); (hi_idx++,hidden=hidden->next)){
		double output=0;

		//For Each hidden node output 
		for(int i=0; i<InputNum; i++){
			output=output+*(input+i)*IH_weight[i][hi_idx];
		}
		output=output+(hidden->threshold);
		output=1/(1+exp(-output));

		//Assign result to Output Node
		hidden->value=output;
	}
}


void OutputEvaluate(Node* hiddenNode){
	
	//Evaluate Output
	for(int i=0; i<OutputNum; i++){
		result[i]=0;
		Node* hidden=hiddenNode->next;
		
		for(int hi_idx=0;  (hi_idx<HiddenNum && hidden!=NULL); (hi_idx++,hidden=hidden->next)){
			result[i]=result[i]+(hidden->value)*(HO_weight[hi_idx][i]);
		}
		result[i]=result[i]+th_output[i];
		result[i]=1/(1+exp(-result[i]));

	}
}


void ErrorEvaluate(int set){

	//Evaluate output node error
	for(int i=0; i<OutputNum; i++){
		 outputErr[i]=result[i] * (1-result[i]) *(output[set][i]-result[i]);
	}

	//Evaluate hidden node error
	for(Node* hidden=HEAD_Hidden->next; hidden!=NULL; hidden=hidden->next){
		double sumErr=0;

		for(int i=0; i<OutputNum; i++){
			sumErr=sumErr+(outputErr[i]*HO_weight[hidden->id][i]);
		}
		sumErr=sumErr*hidden->value*(1-hidden->value);

		hidden->error=sumErr;
	}

}


void ReviseWeight(int set){
	double delta=0;
	
	//Weight [Input->hidden]
	for(int i=0; i<InputNum; i++){
		for(Node* hidden=HEAD_Hidden->next; hidden!=NULL; hidden=hidden->next){
			
			delta=alpha_weight*hidden->error*input[set][i];
			IH_weight[i][hidden->id]=IH_weight[i][hidden->id]+delta;
		}
	}
	
	//Weight [hidden->output]
	for(Node* hidden=HEAD_Hidden->next; hidden!=NULL; hidden=hidden->next){
		for(int i=0; i<OutputNum; i++){

			delta=alpha_weight*outputErr[i]*hidden->value;
			HO_weight[hidden->id][i]=HO_weight[hidden->id][i]+delta;	
		}
	}

	//thershold revise
	for(Node* h=HEAD_Hidden->next; h!=NULL; h=h->next){
		h->threshold=h->threshold+alpha_weight*h->error;
	}
	
	for(int i=0; i<OutputNum; i++){
		th_output[i]=th_output[i]+alpha_weight*outputErr[i];
	}
}


void RUN(){
	
	double EndError=0;
	double testing_input[InputNum];

	//================Init Input, Output, Weight & hidden node
	printf("Init\n");
	AssignIO(path);
	AssignHiddenNode();
	
	//================Training
	printf("Training\n");
	do{
		EndError=0;
		
		for(int i=0; i<SetNum; i++){
			
			MatrixEvaluate(input[i], HEAD_Hidden);		
			OutputEvaluate(HEAD_Hidden);						//output is result[i]

			ErrorEvaluate(i);
			ReviseWeight(i);

			if(output[i][0]>result[0]){
				if((output[i][0]-result[0])*RandRng>EndError){
					EndError=(output[i][0]-result[0])*RandRng;
				}
			}else{
				if((result[0]-output[i][0])*RandRng>EndError){
					EndError=(result[0]-output[i][0])*RandRng;
				}
			}
		}
		printf("Error=%lf\n",EndError);
	}while(EndError>delta_error);
	
	for(int i=0; i<InputNum; i++){
		for(int j=0; j<HiddenNum; j++){
			printf("%lf,",IH_weight[i][j]);
		}
		printf("\n");
	}

	for(int i=0; i<HiddenNum; i++){
		for(int j=0; j<OutputNum; j++){
			printf("%lf,",HO_weight[i][j]);
		}
		printf("\n");
	}

	//================Testing!!!
	while(1){
		printf("Enter your input: ");
		cin>>testing_input[0]>>testing_input[1];
		if(testing_input[0]>1 || testing_input[1]>1){
			break;
		}

		MatrixEvaluate(&testing_input[0], HEAD_Hidden);		
		OutputEvaluate(HEAD_Hidden);						//output is result[i]
		
		printf("Result=%lf\n",result[0]);
	}
}

#ifdef PYLIB
double GetInput(PyObject* list){
	int i, n;
    double total = 0;
    PyObject *item;

    n = PyList_Size(list);
    if (n < 0)
        return -1; 
    for (i = 0; i < n; i++) {
        item = PyList_GetItem(list, i); 
        if (!PyInt_Check(item)) 
			continue; 
        total += PyInt_AsLong(item);
    }
    return total;
}

PyObject* SqrtInPyObj(PyObject* obj){
    int n = PyInt_AsLong(obj);
    return Py_BuildValue("i", n*n);
}

#endif

