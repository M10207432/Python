import sklearn.neural_network as NN_Module
import matplotlib
import numpy as np

class NN_Voc(NN_Module.MLPClassifier):
    def __init__(self):
        print "Neural Network"

        self.x=[]
        self.y=[]
        for i in range(1,10):
            for j in range(1,10):
                self.x.append([i,j])
                self.y.append(i*j)
        '''       
        self.x=[[0.,0.],[1.,1.]] #n_samples,n_features
        self.y=[0,1]            #n_samples
        '''
        self.training()
        self.predict()
        
    def training(self):
        self.clf=NN_Module.MLPClassifier(activation='tanh',solver='lbfgs',alpha=1e-4,
                      hidden_layer_sizes=(5,2), random_state=1)
        self.clf.fit(self.x,self.y)

        for coef in self.clf.coefs_:
            print coef
        
    def predict(self):
        
        Result=self.clf.predict([[5., 2.], [12., 2.]])

        print Result
    
def main():
    VocTrain= NN_Voc()
    


if __name__=="__main__":
    main()
