import params
import time
import random


def generate_data_randomly(nb_criteria, number):
    dict_data = {}
    for i in range(number):
        dict_data[i] =  [[random.uniform(1, 15000) for j in range(nb_criteria)], [], [], 'NR']

    return dict_data

def pref_lin(value_1, value_2, c):
    CRITERIA_MAX = params.get_criteria_MAX()
    CRITERIA_P = params.get_criteria_P()
    CRITERIA_Q = params.get_criteria_Q()

    if(CRITERIA_MAX[c]):
        diff = value_1 - value_2
    else:
        diff = value_2 - value_1
    if(diff > CRITERIA_P[c]):
        return 1
    if(diff <= CRITERIA_Q[c]):
        return 0
    return ((diff - CRITERIA_Q[c])/(CRITERIA_P[c] - CRITERIA_Q[c]))

def compute_unicriteria_flows(data):
    numbers = len(data)
    state = 0
    counter = 0
    for key in data:
        alternative = data[key][0]
        for crit_number in range(len(alternative)):
            unicrit_net_flow = unicriteria_flow_mat(data, alternative, crit_number)
            data[key][1].append(unicrit_net_flow)

def unicriteria_flow_mat(table, alternative, c):
    positive_flow = 0
    negative_flow = 0
    for key in table:
        positive_flow += pref_lin(alternative[c], table[key][0][c], c)
        negative_flow += pref_lin(table[key][0][c], alternative[c], c)
    positive_flow /= (len(table) - 1)
    negative_flow /= (len(table) - 1)
    return (positive_flow - negative_flow)

def compute_total_flows(data):
    weights = params.get_criteria_W()
    for key in data:
        total_flow = 0
        for crit in range(params.get_number_criteria()):
            total_flow += weights[crit] * data[key][1][crit]
        data[key][2] = total_flow

def compute_ranks(data, max_rank):
    list_data = [(key, data[key]) for key in data]
    list_data = sorted(list_data, key=lambda item: item[1][2], reverse=True )
    current_rank = 0
    previous_value = 2
    for item in list_data:
        if previous_value != item[1][2]:
            current_rank += 1
            previous_value = item[1][2]
        item[1][3] = current_rank
        if current_rank > max_rank:
            break

def output_csv_data(filename, data, size_x, size_y):
    fo = open(filename, 'w')
    for x in range(size_x):
        for y in range(size_y):
            key = (x,y)
            line_output = '(' + str(x) + ',' + str(y) + ')'
            line_output += ';'
            line_output += str(data[key][0][0])
            for value in data[key][0][1:]:
                line_output += ',' + str(value)
            line_output += ';'
            line_output += str(data[key][1][0])
            for value in data[key][1][1:]:
                line_output += ',' + str(value)
            line_output += ';'
            line_output += str(float(data[key][2]))
            line_output += ';'
            line_output += str(data[key][3])
            line_output += '\n'
            fo.write(line_output)
    fo.close()

def main():
    fo = open('time_run_out.csv', 'w')

    number = 2
    while True:
        data = generate_data_randomly(params.get_number_criteria(), int(number))
    #    print('Data generated.')
        time_begin = time.time()
    #    print('Computing flows...')
        compute_unicriteria_flows(data)
    #    print('Flows computed.')
        compute_total_flows(data)
    #    print('Total flows computed.')
        fo.write(str(number) + ';' + str(time.time() - time_begin) + '\n')
        fo.flush()
        if time.time() - time_begin > 60*50: #stops if it took more than 50 minutes
            break
        number *= 1.1
    fo.close()


if __name__ == "__main__":
    main()
