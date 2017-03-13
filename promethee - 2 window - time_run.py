import params
import time
from operator import itemgetter, attrgetter, methodcaller
from collections import deque
import random


def generate_data_randomly(nb_criteria, number):
    dict_data = {}
    for i in range(number):
        dict_data[i] =  [[random.uniform(1, 15000) for j in range(nb_criteria)], [], [], 'NR']

    return dict_data


def generate_data(size_x, size_y):
    print(size_x, size_y)
    image_data = {}
    for x in range(size_x):
        for y in range(size_y):
            image_data[(x, y)] = [[], [], [], 'NR']
    print("Data generated")

    return image_data


def output_csv_data(filename, image_data):
    fo = open(filename, 'w')
    for key in image_data:
        line_output = '(' + str(key) + ')'
        line_output += ';'
        line_output += str(image_data[key][0][0])
        for value in image_data[key][0][1:]:
            line_output += ',' + str(value)
        line_output += ';'
        line_output += str(image_data[key][1][0])
        for value in image_data[key][1][1:]:
            line_output += ',' + str(value)
        line_output += ';'
        line_output += str(float(image_data[key][2]))
        line_output += ';'
        line_output += str(image_data[key][3])
        line_output += '\n'
        fo.write(line_output)
    fo.close()


def generate_unicriterion_flow_dict(mat_alt, crit):
    time_begin = time.time()
    unicriterion_flow_dict = {}
    unicriterion_pos_flow_dict = {}
    unicriterion_neg_flow_dict = {}
    values = [item[0][crit] for item in mat_alt.values()]
    values = sorted(values)

    ### Positive flow calculation
    prev_frame = deque()
    waiting_frame = deque()
    current_pos_flow = 0.0
    pref_threshold = params.get_criteria_P()[crit]
    indif_threshold = params.get_criteria_Q()[crit]
    i = 0
    previous_value = 0
    while i < len(values):
        pos_flow_contrib = 0
        current_value = values[i]

        while len(prev_frame) > 0 and current_value - prev_frame[0] >= pref_threshold:
            #remove this value from previous frame and compute flow contribution
            contrib = (pref_threshold - (previous_value - prev_frame[0])) / (pref_threshold - indif_threshold)
            if contrib < 0:
                print("ERROR! Debug info:", contrib, pref_threshold, indif_threshold, previous_value, prev_frame[0])
                input()
            pos_flow_contrib += contrib
            prev_frame.popleft()

        pos_flow_contrib +=  len(prev_frame) * (values[i] - previous_value) / (pref_threshold - indif_threshold)

        while len(waiting_frame) > 0 and current_value - waiting_frame[0] >= indif_threshold:
            contrib = (current_value - waiting_frame[0] - indif_threshold) / (pref_threshold - indif_threshold)
            if contrib < 0:
                print("ERROR! Debug info:", contrib, pref_threshold, indif_threshold, previous_value, prev_frame[0])
                input()
            if contrib > 1:
                contrib = 1
                waiting_frame.popleft()
            else:
                prev_frame.append(waiting_frame.popleft())
            pos_flow_contrib += contrib

        current_pos_flow += pos_flow_contrib / (len(values) - 1)
        unicriterion_pos_flow_dict[current_value] = current_pos_flow

#        print("Current pos flow: " + str(current_pos_flow) + ' - iteration: ' + str(i) + ' - value: ' + str(current_value))
        while i < len(values) and values[i] == current_value:
            waiting_frame.append(values[i])
            i += 1
        previous_value = current_value

    ### Negative flow calculation
    values = sorted(values, reverse=True)
    prev_frame = deque()
    waiting_frame = deque()
    current_neg_flow = 0.0
    pref_threshold = params.get_criteria_P()[crit]
    indif_threshold = params.get_criteria_Q()[crit]
    i = 0
    previous_value = 0
    while i < len(values):
        neg_flow_contrib = 0
        current_value = values[i]

        while len(prev_frame) > 0 and prev_frame[0] - current_value >= pref_threshold:
            #remove this value from previous frame and compute flow contribution
            contrib = (pref_threshold - (prev_frame[0] - previous_value)) / (pref_threshold - indif_threshold)
            if contrib < 0:
                print(contrib, pref_threshold, indif_threshold, previous_value, prev_frame[0])
                input()
            neg_flow_contrib += contrib
#            print('Contribution sortie : ' + str(contrib))
            prev_frame.popleft()

        neg_flow_contrib +=  len(prev_frame) * (previous_value - values[i]) / (pref_threshold - indif_threshold)

        while len(waiting_frame) > 0 and waiting_frame[0] - current_value >= indif_threshold:
            contrib = (waiting_frame[0] - current_value - indif_threshold) / (pref_threshold - indif_threshold)
            if contrib < 0:
                print(contrib, pref_threshold, indif_threshold, previous_value, prev_frame[0])
                input()
            if contrib > 1:
                contrib = 1
                waiting_frame.popleft()
            else:
                prev_frame.append(waiting_frame.popleft())
            neg_flow_contrib += contrib
#            print('Contribution entrée : ' + str(contrib))

#        print(neg_flow_contrib)
        current_neg_flow += neg_flow_contrib / (len(values) - 1)
        unicriterion_neg_flow_dict[current_value] = current_neg_flow

#        print("Current neg flow: " + str(current_neg_flow) + ' - iteration: ' + str(i) + ' - value: ' + str(current_value))
        while i < len(values) and values[i] == current_value:
            waiting_frame.append(values[i])
            i += 1
        previous_value = current_value
#    print(unicriterion_neg_flow_dict)
#    input()
    for key in unicriterion_pos_flow_dict:
        unicriterion_flow_dict[key] = unicriterion_pos_flow_dict[key] - unicriterion_neg_flow_dict[key]
#    print(unicriterion_flow_dict)

#    print('Ellapsed time - unicriterion flow computation: ' + str(time.time() - time_begin) + ' seconds')
    return unicriterion_flow_dict

def compute_flow(mat_alt):
    time_begin = time.time()
    for crit_number in range(params.get_number_criteria()):
        unicriteria_flow_dict = generate_unicriterion_flow_dict(mat_alt, crit_number)
        for key in mat_alt:
            unicrit_flow_value = unicriteria_flow_dict[get_criteria_value(mat_alt[key])[crit_number]]
            mat_alt[key][1].append(unicrit_flow_value)
    for key in mat_alt:
        total_flow = 0.0
        for crit_number in range(params.get_number_criteria()):
            unicrit_flow_value = mat_alt[key][1][crit_number]
            total_flow += params.get_criteria_W()[crit_number] * unicrit_flow_value
        mat_alt[key][2] = total_flow


def get_criteria_value(alternative):
    return alternative[0]


def main():
    time_begin = time.time()
    fo = open('time_run_window_out.csv', 'w')

    number = 2
    while True:

        image_data = generate_data_randomly(params.get_number_criteria(), int(number))
    #    print('Data generated.')
        time_begin = time.time()
    #    print('Computing flows...')
        compute_flow(image_data)

        fo.write(str(number) + ';' + str(time.time() - time_begin) + '\n')
        fo.flush()
        if time.time() - time_begin > 60*50 or number > 4000000: #stops if it took more than 50 minutes or more than 4M alternatives (memory issue)
            break
        number *= 1.1
    fo.close()


if __name__ == "__main__":
    main()
