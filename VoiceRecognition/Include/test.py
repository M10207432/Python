import matplotlib.pyplot as plt
import numpy as np

from sklearn import datasets, svm, metrics
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

class SVM_Machine():
  def __init__(self):
    print "SVM Machine"

  def training(self):
    digits = datasets.load_digits()

    sample_size=len(digits.images)
    data=digits.images.reshape((sample_size,-1))
    
    print digits.images[0]
    print "=================="
    print data[0]

    min_value=1
    min_max=0.0
    save_para=1.0
    para=0.001
    #Create SVM machine
    classifier = svm.SVC(gamma=para)

    #Training...
    classifier.fit(data[:sample_size/2],digits.target[:sample_size/2])

    #Predict data & Expected data
    expected = digits.target[sample_size/2:]
    predicted = classifier.predict(data[sample_size/2:])

    #Show the result
      
    print("Confusion matrix:\n%s"
          % metrics.confusion_matrix(expected,predicted))
    print("Classification report %s:\n%s\n"
          %(classifier, metrics.classification_report(expected, predicted)))
      
    '''
      machine=metrics.confusion_matrix(expected,predicted)
    
      for i,pre_data in enumerate(machine):
        total_value=sum(pre_data)
        if float(min_value) > (float(pre_data[i])/float(total_value)):
          min_value = (float(pre_data[i])/float(total_value))
      if min_value>min_max:
        print min_value
        save_para=para
        min_max=min_value
    '''
    #print "Parameter:",save_para
    #print "Min Max:",min_max

  def retrieve():
    digits = datasets.load_digits()

    #Lookup data structure
    for key,value in digits.items():
      try:
        print key,value.shape
      except:
        print key

    #Arrange raw_data & target
    img_label = list(zip(digits.images, digits.target))

    for i,(img,label) in enumerate(img_label[:5]):
      plt.subplot(2,4,i+1)
      plt.axis("off")
      plt.imshow(img,cmap=plt.cm.gray_r, interpolation='nearest')
      plt.title("Train: %i" % label)
    plt.show()
  
class LDA_Machine():
  def __init__(self):
    print "LDA"
    
  def genearate_data(self,sample_len, feature_len):
    X,y=datasets.make_blobs(n_samples=sample_len, n_features=1, centers=[[-2],[2]])
    if feature_len > 1:
      X=np.hstack([X, np.random.randn(sample_len, feature_len-1)])
    return X,y
  
  def chg_feature(self,n_sample,n_feature_max,step,avg):
    lda1=[]
    lda2=[]
    
    for n_feature in range(1,n_feature_max+1,step):
      lda1_sum=0
      lda2_sum=0
      
      for i in range(avg):
        #For Training
        X,y=self.genearate_data(n_sample, n_feature)

        lda1_machine=LinearDiscriminantAnalysis(solver='lsqr', shrinkage='auto').fit(X,y)
        lda2_machine=LinearDiscriminantAnalysis(solver='lsqr', shrinkage=None).fit(X,y)

        #For Testing
        X,y=self.genearate_data(n_sample, n_feature)

        lda1_sum=lda1_machine.score(X,y)
        lda2_sum=lda2_machine.score(X,y)
      lda1.append(lda1_sum/avg)
      lda2.append(lda2_sum/avg)
    return lda1,lda2
class IRIS():
  def __init__(self):
    print "Iris classifier"
    
  def load_data(self):
    iris_dict=datasets.load_iris()

    self.X=iris_dict.data[:,0:2]
    self.y=iris_dict.target

    self.n_samples=self.X.shape[0]
    self.n_features=self.X.shape[1]

    #Get feature matrix all compose
    xx,yy=np.meshgrid(np.linspace(3,9,100),np.linspace(1,5,100).T)
    self.Xfull=np.c_[xx.ravel(),yy.ravel()]
    
    for key,value in iris_dict.items():
      try:
        print key,value.shape
      except:
        print key
        
  def training(self):
    C=1.0
    classifiers={"L1":LogisticRegression(C=C, penalty='l1'),
                 "L2_OVR":LogisticRegression(C=C, penalty='l2'),
                 "Linear":SVC(kernel='linear', C=C, probability=True, random_state=0),
                 "L2_MUL":LogisticRegression(C=C, solver='lbfgs',multi_class="multinomial")}
    n_classifiers=len(classifiers)
    
    fig=plt.figure(figsize=(12,12),dpi=300)
    
    for i , (name,classifier) in enumerate(classifiers.items()):

      classifier.fit(self.X,self.y) #Training
      y_pred=classifier.predict(self.X)  #Test

      classifier_rate=np.mean(y_pred.ravel()==self.y.ravel())*100
      print "Classfifier",name,classifier_rate

      #View
      probas=classifier.predict_proba(self.Xfull)
      
      n_classes=np.unique(y_pred).size
      
      for k in range(n_classes):
        plt.subplot(n_classifiers, n_classes, i*n_classes+k+1)
        plt.title("class %d" % k)
        
        if k==0:
          plt.ylabel(name)
        imshow_handle = plt.imshow(probas[:,k].reshape((100,100)),
                                   extent=(3,9,1,5),
                                   origin='lower')
        plt.xticks(())
        plt.yticks(())
        idx = (y_pred==k)
        if idx.any():
          plt.scatter(self.X[idx,0], self.X[idx,1], marker='o', c='k')

    ax=plt.axes([0.15,0.04,0.7,0.05])
    plt.title('Probability')
    plt.colorbar(imshow_handle, cax=ax, orientation='horizontal')

    plt.show()
        
      
    
def main():
  print "Boot"
  '''
  LDA=LDA_Machine()
  lda1,lda2=LDA.chg_feature(10,5,1,10)
  print lda1,lda2
  '''
  Iris_sample=IRIS()
  Iris_sample.load_data()
  Iris_sample.training()


  
if __name__=="__main__":
  main()
