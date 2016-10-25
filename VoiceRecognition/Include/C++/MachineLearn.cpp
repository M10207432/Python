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
double th_output[OutputNum];
double IH_weight[InputNum][HiddenNum];
double HO_weight[HiddenNum][OutputNum];

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
			IH_weight[i][j]=(double)(rand()%(RandRng*2))/RandRng-1;
		}
	}

	//Hidden to Output Arrange [rand() from -1~1]
	for(int i=0; i<HiddenNum; i++){
		for(int j=0; j<OutputNum; j++){
			HO_weight[i][j]=(double)(rand()%(RandRng*2))/RandRng-1;
		}
	}

	//Output threshold [rand() from -1~1]
	for(int i=0; i<OutputNum; i++){
		th_output[i]=(double)(rand()%(RandRng*2))/RandRng-1;
	}

}

void AssignHiddenNode(){
	HEAD_Hidden=(Node *)malloc(sizeof(Node));
	Node* tmp=HEAD_Hidden;
	
	//Assign Hidden layer link list
	tmp->next=NULL;
	for(int i=0; i<HiddenNum; i++){
		Node* n=(Node *)malloc(sizeof(Node));
		n->threshold=(double)(rand()%(RandRng*2))/RandRng-1;

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
		output=1/(1+exp(output));

		//Assign result to Output Node
		hidden->value=output;
	}
}
void OutputEvaluate(Node* hiddenNode, double *output){
	double result;
	
	for(int i=0; i<OutputNum; i++){
		result=0;
		 Node* hidden=hiddenNode->next;
		
		 for(int hi_idx=0;  (hi_idx<HiddenNum && hidden!=NULL); (hi_idx++,hidden=hidden->next)){
			result=result+(hidden->value)*(HO_weight[hi_idx][i]);
		}
		 result=result+th_output[i];
		 result=1/(1+exp(result));

		 //Assign result to Output Node
		output[i]=result;
	}

}

void RUN(){
	
	AssignIO(path);
	AssignHiddenNode();
	
	//Evaluate for hidden node
	for(int i=0; i<SetNum; i++){
		MatrixEvaluate(input[i], HEAD_Hidden);
		OutputEvaluate(HEAD_Hidden,output[i]);



	}

	//Evaluate for output


	
}


double Add(double n1, double n2){
	return n1+n2;
}

float Div(float n, float div){
	return n/div;
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

