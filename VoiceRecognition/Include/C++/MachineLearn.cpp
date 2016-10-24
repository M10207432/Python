#include "MachineLearn.h"
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <fstream>
#include <iostream>

using namespace std;
/*======================
	Global Variable
======================*/

double input[TestSetNum][InputNum];			//last one for end
double output[TestSetNum][OutputNum];	//last one for end

/*======================
						Function
======================*/
void AssignIO(char * path){
	ifstream  file;

	//Open file & Arrange structure
	file.open(path,ios::in);

	for(int set_id=0; set_id<TestSetNum;set_id++){
		for(int i=0; i<InputNum; i++){
			file>>input[set_id][i];
		}
		for(int j=0; j<OutputNum; j++){
			file>>output[set_id][j];
		}
	}

	//Show data
	for(int set_id=0; set_id<TestSetNum;set_id++){
		for(int i=0; i<InputNum; i++){
			cout<<input[set_id][i]<<endl;;
		}
		for(int j=0; j<OutputNum; j++){
			cout<<output[set_id][j]<<endl;
		}
	}
}

void AssignHiddenNode(){
	Node* HEAD_Hidden=(Node *)malloc(sizeof(Node));
	Node* tmp;

	//Assign Hidden layer link list
	tmp=HEAD_Hidden;
	tmp->next=NULL;
	for(int i=0; i<HiddenNum; i++){
		Node* n=(Node *)malloc(sizeof(Node));
		n->weight=init_weight;
		n->threshold=init_th;

		tmp->next=n;
		tmp=n;
	}
	tmp->next=NULL;
}


double* MatrixEvaluate(double* input, double *hiddenNode, double *Hidden_th){
	int input_num=0;
	int weight_num=0;
	int output_num=0;
	double *OutputMatrix;

	/*----------------------------------
			Evaluate Output Number &
			Assign space for filling in
	----------------------------------*/
	for(double *input_ptr=input; *input_ptr!=EndVal; input_ptr++){
			input_num++;
	}
	for(double *w=hiddenNode; *w!=EndVal; w++){
		weight_num++;
	}
	output_num=weight_num/input_num;
	OutputMatrix=(double *)malloc(output_num);

	/*----------------------------------
			Evaluate Ouput &
			Assign value 
	----------------------------------*/
	for(double *w=hiddenNode; *w!=EndVal;){
		double output=0;

		//For Each hidden node output [increase input_ptr & w]
		for(double *input_ptr=input; *input_ptr!=EndVal; input_ptr++,w++ ){
			output=output+(*input_ptr)*(*w);
		}
		output=output+(*Hidden_th++);
		output=1/(1+exp(output));

		//Assign result to Output Node
		(*OutputMatrix)=output;
		OutputMatrix++;
	}

	return OutputMatrix;
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

