#include "MachineLearn.h"

/*======================
	Global Variable
======================*/

double input[InputNum];
double weight[InputNum+HiddenNum][HiddenNum];

/*======================
		Function
======================*/
void weightEvaluate(int start, int end_id, struct _hiddennode* node){
	
	int target_id=node->id;
	double output=0;
	
	for(int id=start; id<=end_id; id++){
		output+=weight[id][target_id]*input[id];
	}
	
	output+=node->threshold;
	
	node->output=output;	
}


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

double Add(double n1, double n2){
	return n1+n2;
}

float Div(float n, float div){
	return n/div;
}

PyObject* SqrtInPyObj(PyObject* obj){
    int n = PyInt_AsLong(obj);
    return Py_BuildValue("i", n*n);
}
