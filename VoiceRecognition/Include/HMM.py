import sys
import numpy

start={"Sunny":0.4,"Rainy":0.6}
State={"Sunny":{"Sunny":0.4,"Rainy":0.6},"Rainy":{"Sunny":0.3,"Rainy":0.7}}#State=[[0.6,0.4],[0.3,0.7]]
Hidden_State={"Rainy":{"Walk":0.1,"Shop":0.4,"Clean":0.5},"Sunny":{"Walk":0.6,"Shop":0.3,"Clean":0.1}} #Emission=[[],[]]

def Viterbi(steps):
    result={}
    
    for i in range(len(steps)):
        Hidden_target=steps[i]
        
        if i==0:    #First time
            for k in start.keys():
                result[k]=start[k]*Hidden_State[k][Hidden_target]
        else:       #Through Pass
            for through in State.keys():
                tmp=0
                for k in start.keys():
                    print start[k],State[k][through],Hidden_State[through][Hidden_target]
                    tmp=max(tmp, start[k]*State[k][through]*Hidden_State[through][Hidden_target])
                result[through]=tmp
                
        for k in result.keys():
            start[k]=result[k]
        print start
        
def main():
    print "HMM"
    
    steps=["Walk","Walk","Shop","Clean"]
    Viterbi(steps)

if __name__=="__main__":
    main()
