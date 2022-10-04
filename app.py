import flask
import pandas as pd
import pickle
import sklearn


def chargeTheModel(pretrainedModel,model):
    # Use pickle to load in the pre-trained model
    print('models/'+pretrainedModel+'_'+model+'.pkl')
    with open(f'models/'+pretrainedModel+'_'+model+'.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def getEmbeddings(file,pretrainedModel):
    df= pd.read_csv ('D:/PFEMaster/EmbeddingVectors/'+pretrainedModel+'_filesEmbeddingsMergeMean.csv') 
    # selecting rows based on condition 
    rslt_df = df.loc[df['commitId'] ==file[:-5]].reset_index()
    return rslt_df 

def getModelMetrics(pretrainedModel,model):
    modelsResults={ 'CodeT5':{'regressionL':[0.82,0.73,0.88,0.78],'svm':[0.91,0.55,0.88,0.68],'naiveBayes':[0.75,0.17,0.62,0.27],'decisionTree':[0.67,0.66,0.74,0.66]},
                    'GraphCodeBert':{'regressionL':[0.77,0.69,0.84,0.73],'svm':[0.88,0.39,0.82,0.54],'naiveBayes':[0.35,0.97,0.48,0.52],'decisionTree':[0.60,0.61,0.69,0.60]},
                    'CodeGPT':{'regressionL':[0.72,0.72,0.85,0.72],'svm':[0.88,0.43,0.82,0.58],'naiveBayes':[0.75,0.28,0.76,0.41],'decisionTree':[0.54,0.52,0.63,0.53]},
                    'UniXCoder':{'regressionL':[0.61,0.63,0.75,0.62],'svm':[0.79,0.30,0.73,0.43],'naiveBayes':[0.74,0.33,0.67,0.46],'decisionTree':[0.58,0.52,0.64,0.55]},
                    'CodeBert':{'regressionL':[0.57,0.72,0.76,0.64],'svm':[0.81,0.46,0.70,0.59],'naiveBayes':[0.35,0.98,0.49,0.52],'decisionTree':[0.65,0.60,0.71,0.62]}
                    }
    
    return modelsResults[pretrainedModel][model]
    


    


app = flask.Flask(__name__,template_folder='template')
app = flask.Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='template')

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        # Just render the initial form, to get input
        return(flask.render_template('index.html'))
    
    if flask.request.method == 'POST':
        # Extract the input
        #"temperature = flask.request.form['temperature']
        file=flask.request.form['fichier']
        pretrainedModel=flask.request.form['pretrainedModels']
        classificationModel=flask.request.form['classification']
    
        df= getEmbeddings(file,pretrainedModel)
        
        #get the caracteristics
        vecteur= df.copy()
        vecteur.drop("Repo", axis=1, inplace=True)
        vecteur.drop('commitId', axis=1, inplace=True)
        vecteur.drop('commitType', axis=1, inplace=True)
        vecteur.drop('index',axis=1, inplace=True)
        
        #get the original classe
        classe=df.copy()
        classe.drop(classe.columns.difference(['commitType']), 1, inplace=True)
        
        if classe["commitType"].iloc[0] ==1 :
            originalClasse= 'Patch Vulnérable'
        else: 
            originalClasse= 'Patch Non Vulnérable'
            
            
        #get the prediction
        model=chargeTheModel(pretrainedModel,classificationModel)
        prediction=model.predict(vecteur)[0]
        
        if prediction ==1 :
            predictionClasse= 'Patch Vulnérable'
        else: 
            predictionClasse= 'Patch Non Vulnérable'
        
        modelMetrics=getModelMetrics(pretrainedModel,classificationModel)
        print(modelMetrics)
             

        return flask.render_template('index.html',predictionClasse=predictionClasse,originalClasse=originalClasse,precision=modelMetrics[0]*100,recall=modelMetrics[1]*100,acc=modelMetrics[2]*100,f1=modelMetrics[3]*100)

if __name__ == '__main__':
    app.run()
