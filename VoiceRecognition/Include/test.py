import matplotlib.pyplot as plt
from sklearn import datasets, svm, metrics
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import numpy as np


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
    
def main():
  print "Boot"
  LDA=LDA_Machine()
  lda1,lda2=LDA.chg_feature(10,5,1,10)
  print lda1,lda2
  
if __name__=="__main__":
  main()
