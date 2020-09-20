import pickle
import numpy as np
import os
import pandas as pd
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

# collecting all csv files from forwarded directory
def collect_csv_data_collection_from_directory(path):

    data_collection = []

    for csv_name in os.listdir(os.path.abspath(path)):
        csv_path = os.path.join(path, csv_name)
        data = pd.read_csv(csv_path, names=['Duration', 'AOI', 'Question'], skip_blank_lines=True, skiprows=[0])
        data_collection.append(data)
    return data_collection

# saving csv files into forwarded path
def save_data_as_csv(data, path):
    import csv

    filename = os.path.join(path + ".tsv")
    with open(filename, "w", newline='') as f:
        writer = csv.writer(f, delimiter = '\t')
        writer.writerows(data)

# get total num of seconds
def total_secons_in_question(duration):
    return sum(duration)

# get no. of regions
def total_regions_in_question(aoi):
    return len(aoi)

# get sec on all regions [vector]
def seconds_per_region(duration, aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 }
    
    for i in range(0, len(duration)):
        vector[aoi[i]] += duration[i]

    return list(vector.values())

# get no. of looks at all regions [vector]
def no_looks_per_region(aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 }
    
    for i in range(0, len(aoi)):
        vector[aoi[i]] += 1

    return list(vector.values())

# mean sec by regions [vector]
def mean_seconds_per_region(duration, aoi):
    from statistics import mean
    
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod': [], 'odgovori': [], 'pitanje': [], 'pitanje-kod': [], 'prazno': [], 'prethodno': [], 'sledece': [] }
    
    for i in range(0, len(aoi)):
        vector[aoi[i]].append(duration[i])

    rez_vector = []
    for v in vector.values():
        if not v:
            rez_vector.append(0.0)
        else:
            rez_vector.append(mean(v))
    
    return rez_vector

# get top viewed region before region x (for all regions) [vector]
def top_region_before_per_region(duration, aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod':
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'odgovori': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'pitanje': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'pitanje-kod': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'prazno': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'prethodno': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'sledece': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 }
            }
    
    previous = aoi[0]

    # move through all regions except first one and add 1 for curren area whose previous one was "previous" area
    for i in range(1, len(aoi)):
        vector[aoi[i]][previous] += 1
        previous = aoi[i]
    
    vector = list(vector.values())
    ret_vector = []

    # loop each area vector and extract area postion wich was the top rated area that commed before current area
    for set_vector in vector:
        values = list(set_vector.values())
        
        if (set(values) == {0.0}):
            ret_vector.append(-1.0)
        else:
            ret_vector.append(values.index(max(values)))

    return ret_vector

# get top viewed region after region x (for all regions) [vector]
def top_region_after_per_region(duration, aoi):
    # regije su: kod, odgovori, pitanje, pitanje-kod, prazno, prethodno, sledece
    vector = { 'kod':
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'odgovori': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'pitanje': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'pitanje-kod': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'prazno': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'prethodno': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 },
            'sledece': 
                { 'kod': 0.0, 'odgovori': 0.0, 'pitanje': 0.0, 'pitanje-kod': 0.0, 'prazno': 0.0, 'prethodno': 0.0, 'sledece': 0.0 }
            }
    
    current = aoi[0]

    # move through all regions except first and last one and add 1 for "curren" area whose previous one was this area
    for i in range(1, len(aoi)):
        vector[current][aoi[i]] += 1
        current = aoi[i]
    
    vector = list(vector.values())
    ret_vector = []

    # loop each area vector and extract area postion wich was the top rated area that commed before current area
    for set_vector in vector:
        values = list(set_vector.values())
        
        if (set(values) == {0.0}):
            ret_vector.append(-1.0)
        else:
            ret_vector.append(values.index(max(values)))

    return ret_vector

# group all info in one vector
def call_information_methods(duration, aoi, question_id):
    vector = []

    i1 = total_secons_in_question(duration)
    i2 = total_regions_in_question(aoi)
    i3 = seconds_per_region(duration, aoi)
    i4 = no_looks_per_region(aoi)
    i5 = mean_seconds_per_region(duration, aoi)
    i6 = top_region_before_per_region(duration, aoi)
    i7 = top_region_after_per_region(duration, aoi)

    vector.append(question_id[0])
    vector.append(i1)
    vector.append(i2)
    vector.extend(i3)
    vector.extend(i4)
    vector.extend(i5)
    vector.extend(i6)
    vector.extend(i7)

    return vector

# get vector of question statistics based on question
def get_question_based_information_vector(data):

    duration = data[data.columns[0]]
    AOI = data[data.columns[1]]
    question_id = data[data.columns[2]]

    vector = call_information_methods(duration, AOI, question_id)
    return vector

# ad row and column label to vector
def add_labels_to_vector(vector):
    df = pd.DataFrame(vector,
                    columns=['question_id', '0', '1', '2', '3', '4', '5','6',
    '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
    '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
    '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'])


    return [df.columns.values.tolist()] + df.values.tolist()

# save classification model to file named 'pickle_model.pkl'
def save_model(model):
    pkl_filename = "pickle_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(model, file)

# load classification model from file named 'pickle_model.pkl'
def load_model():
    pkl_filename = "pickle_model.pkl"
    with open(pkl_filename, 'rb') as file:
        pickle_model = pickle.load(file)
    return pickle_model


# MAIN
print("\n\r\n\r")
information_vector = []

collected_data = collect_csv_data_collection_from_directory("./gaze_dataset/csv/")
for i in range(0, len(collected_data)):
    current_info = get_question_based_information_vector(collected_data[i])
    information_vector.append(current_info)

full_dataset = pd.read_csv('./gaze_dataset/full_info_dataset.csv', sep=',',header=0)
full_dataset = full_dataset.drop(columns=["Question"])
#train, test = train_test_split(full_dataset, test_size=0.2, random_state=42, shuffle=False)
train = full_dataset.sample(frac=0.8,random_state=42)
test = full_dataset.drop(train.index)

y_tr = train.iloc[:,0]
X_tr = train.iloc[:,1:]

y_test = test.iloc[:,0]
X_test = test.iloc[:,1:]

LR = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial', max_iter = 5000).fit(X_tr, y_tr)
LR.predict(X_test)
rez = LR.score(X_test,y_test)
print("LogisticRegression: " + str(round(LR.score(X_test,y_test), 4)))

SVM = svm.SVC(decision_function_shape="ovo", max_iter = 5000).fit(X_tr, y_tr)
SVM.predict(X_test)
print("SVM: " + str(round(SVM.score(X_test, y_test), 4)))

RF = RandomForestClassifier(n_estimators=1000, max_depth=10, random_state=0).fit(X_tr, y_tr)
RF.predict(X_test)
print("RandomForestClassifier: " + str(round(RF.score(X_test, y_test), 4)))

NN = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15000, 10), random_state=1, max_iter = 5000).fit(X_tr, y_tr)
NN.predict(X_test)
print("MLPClassifier: " + str(round(NN.score(X_test, y_test), 4)))

# save best model which is LR -> acc = 0.7391
save_model(LR)
loaded_model = load_model()
LR.predict(X_test)
rez = LR.score(X_test,y_test)
print("Loaded LogisticRegression: " + str(round(LR.score(X_test,y_test), 4)))
