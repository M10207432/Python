#include "MachineLearn.h"

int AddOne(int n){
    return n+1;
}

int Sqrt(int n){
    return n*n;
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
