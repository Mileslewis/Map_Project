import pandas as pd
import numpy as np
import plotly.express as px
import math

from Features import Features
from Labels import Labels
from Models import Models

ML = True

df = pd.read_csv("Data/summer.csv",index_col=0)
df["sin_lat"] = df["lat"].apply(math.radians).apply(math.sin)
df["cos_lat"] = df["lat"].apply(math.radians).apply(math.cos)
df = df.drop(["lat","long","rain"],axis = 1)
df["const"] = 1
df["temp"]= (df["temp"] - df["temp"].min())/ max(df["temp"].max() - df["temp"].min(),0.001)

below = df[df["elevation"] <= 0]
above = df[df["elevation"] > 0]
below["elevation"]= (below["elevation"] - df["elevation"].min())/ max(df["elevation"].max() - df["elevation"].min(),0.001)
above["elevation"]= (above["elevation"] - df["elevation"].min())/ max(df["elevation"].max() - df["elevation"].min(),0.001)
print(below)

ar1,ar2,ar3,ar4,test = np.array_split(above.sample(frac = 1),5)
train = pd.concat([ar1,ar2,ar3,ar4])

train_labels = train['temp'].values.tolist()
train = train.drop(columns=['temp'])

test_labels = test['temp'].values.tolist()
test = test.drop(columns=['temp'])

    # turn df into list for use as features.data
train_f = []
for c in train.columns:
    train_f.append(list(train[c].values))
#print(len(train_f))
#print(len(train_f[0]))

test_f = []
for c in test.columns:
    test_f.append(list(test[c].values))
#print(len(test_f))
#print(len(test_f[0]))

    # create features
train_features = Features(train_f)
test_features = Features(test_f)

initial_model = Models()
initial_model.initialize_model(train_features)
#initial_model.add_layer(neurons = 5,activation = "sigmoid")
initial_model.randomize_model()

learning_rate = [0.0004]
batch = [20]
repeats =50
cutoff = 100000
l1 = 0
l2 = 0.002

    # hold data for creating graph
df2 = pd.DataFrame()
columns = []
location = 0

if ML:
    for L in learning_rate:
        for B in batch:
    # copy initial model to test hyperparameters from same start
            model = initial_model.copy()
            # print(f"0: {model}")
            total_losses = []
            iteration = 0
            while iteration < repeats:
    # update model once through all features and record total loss for graph
                total_losses.append(
                    model.update(train_features, train_labels, B, L, l2, l1)
                )
                # print(f"{iteration+1}: {model}")
    # if the model has deconverged then cutoff
                if total_losses[iteration] > cutoff:  
                    for i in range(iteration + 1, repeats):
                        total_losses[iteration] = cutoff
                        total_losses.append(cutoff)
                    break

                iteration = iteration + 1
                #print("iteration : "+str(iteration))
                #model.print_model()
                #print("average_loss:")
                #print(model.test(features = train_features,labels = train_labels))

            column = f"batch size: {B}, learning rate: {L}"
            df2.insert(location, column, total_losses)
            location = location + 1
            columns.append(column)
        
            #print(f"batch size: {B}, learning rate: {L}, final average log loss: {model.test(features,labels)}")
    # print graph showing loss curves for each model
    px.line(
        df2,
        y=[x for x in columns],
        title="Total log loss at each epoch for Initial Model with different Batch Sizes/Learning Rates",
        labels={"value": "log loss", "index": "epoch"},
        log_y=True,
    ).show()

    # print and test final model (used once final hyperparameters are decided)
    print("final_model:")
    model.print_model()
    print("average_loss:")
    # model.test() returns: ave_loss, TP, FP, FN, TN
    print(model.test(features = test_features,labels = test_labels,return_confusion = False, threshold = 0.5))
