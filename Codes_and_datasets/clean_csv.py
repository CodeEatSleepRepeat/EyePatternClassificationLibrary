import numpy as np
import pandas as pd
import os

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


def add_labels_to_vector(vector):
    df = pd.DataFrame(vector,
                    columns=['question_id', '0', '1', '2', '3', '4', '5','6',
    '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
    '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
    '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'])


    return [df.columns.values.tolist()] + df.values.tolist()

# MAIN

information_vector = []

collected_data = collect_csv_data_collection_from_directory("./gaze_dataset/csv/")
for i in range(0, len(collected_data)):
    current_info = get_question_based_information_vector(collected_data[i])
    information_vector.append(current_info)


save_data_as_csv(add_labels_to_vector(information_vector), "./gaze_dataset/filtered_csv/question_stats_rows")

print("End of code")