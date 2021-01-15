import sys

train_data_file = sys.argv[1]
test_data_file = sys.argv[2]
feature_file = sys.argv[3]
k = sys.argv[4]


def create_feature_vectors_files(file_name, k_features):
    vector_output_file_name = file_name + ".vector"

    data_file = open('./Sentiment/' + file_name, 'r')
    vector_output_file = open(vector_output_file_name, 'w')

    data = data_file.readlines()

    feature_vectors = ""
    feature_vector = []
    label = True
    for line in data:
        if line != "\n":
            line = line.strip("\n")
            if label:
                feature_vector.append(int(line))
                label = False
            elif line in k_features:
                index = k_features.index(line)
                feature_vector.append(index + 1)
        else:
            label = True
            if len(feature_vector) != 0:
                feature_vector.sort()
                for feature_id_index in range(0, len(feature_vector)):
                    if feature_id_index == 0:
                        feature_vector[feature_id_index] = str(feature_vector[feature_id_index])
                    else:
                        feature_vector[feature_id_index] = str(feature_vector[feature_id_index]) + ":1"
                feature_vector = list(dict.fromkeys(feature_vector))
                feature_vector_sparse = ' '.join(feature_vector)
                if len(feature_vector_sparse) == 1:
                    feature_vector_sparse += " "
                #print(feature_vector_sparse)
                feature_vectors += feature_vector_sparse + "\n"
                feature_vector = []

    if len(feature_vector) != 0:
        feature_vector.sort()
        for feature_id_index in range(0, len(feature_vector)):
            if feature_id_index == 0:
                feature_vector[feature_id_index] = str(feature_vector[feature_id_index])
            else:
                feature_vector[feature_id_index] = str(feature_vector[feature_id_index]) + ":1"
        feature_vector = list(dict.fromkeys(feature_vector))
        feature_vector_sparse = ' '.join(feature_vector)
        if len(feature_vector_sparse) == 1:
            feature_vector_sparse += " "
        feature_vectors += feature_vector_sparse

    vector_output_file.write(feature_vectors)
    vector_output_file.close()


feature_data = open('./Sentiment/' + feature_file, 'r')

features = feature_data.readlines()
k_features = []
for i in range(0, int(k)):
    k_features.append(features[i].strip("\n"))


create_feature_vectors_files(train_data_file, k_features)
create_feature_vectors_files(test_data_file, k_features)
