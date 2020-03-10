
# coding: utf-8

# In[1]:

import collections


# In[2]:

Result = collections.namedtuple("Result", ["score", "message"])


# In[3]:

def ccks2018_1(sub_file, result_file):
    if sub_file[-3:] == 'zip':
        sub_file = extract_zip(sub_file, file_type='.txt')
    with open(sub_file, 'r') as f1, open(result_file, 'r') as f2:
        sub_data = f1.readlines()
        res_data = f2.readlines()
    dict_sub = {}
    dict_res = {}
    row = 0
    row_line = 0
    for sub_line in sub_data:
        row += 1
        if len(sub_line.strip()) > 0:
            row_line += 1
            if len(sub_line.split(',')[1:]) >= 1:
                dict_sub[sub_line.split(',', 1)[0]] = sub_line.split(',')[1]
            else:
                return Result(-1, 'Line ' + str(row) + ' error in ID format')
    for res_line in res_data:
        if len(res_line.strip()) > 0:
            dict_res[res_line.split(',', 1)[0]] = res_line.split(',')[1]
    if row_line != len(dict_res):
        return Result(-1, 'out of data')
    anatomy_dict, symptom_dict, independent_dict, drugs_dict, operation_dict = {}, {}, {}, {}, {}
    anatomy_g, symptom_g, independent_g, drugs_g, operation_g, overall_g = 0, 0, 0, 0, 0, 0
    for row_id in dict_res:
        if row_id not in dict_sub:
            return Result(-1, 'Incorrect ID in line: ' + str(row_id))
        t_lst = dict_res[row_id].split(';')[:-1]
        for item in t_lst:
            item = item.split('\t')
            overall_g += 1
            if item[3] == '解剖部位':
                anatomy_g += 1
                if row_id not in anatomy_dict:
                    anatomy_dict[row_id] = []
                    anatomy_dict[row_id].append(item[:3])
                else:
                    anatomy_dict[row_id].append(item[:3])
            elif item[3] == '症状描述':
                symptom_g += 1
                if row_id not in symptom_dict:
                    symptom_dict[row_id] = []
                    symptom_dict[row_id].append(item[:3])
                else:
                    symptom_dict[row_id].append(item[:3])
            elif item[3] == '独立症状':
                independent_g += 1
                if row_id not in independent_dict:
                    independent_dict[row_id] = []
                    independent_dict[row_id].append(item[:3])
                else:
                    independent_dict[row_id].append(item[:3])
            elif item[3] == '药物':
                drugs_g += 1
                if row_id not in drugs_dict:
                    drugs_dict[row_id] = []
                    drugs_dict[row_id].append(item[:3])
                else:
                    drugs_dict[row_id].append(item[:3])
            elif item[3] == '手术':
                operation_g += 1
                if row_id not in operation_dict:
                    operation_dict[row_id] = []
                    operation_dict[row_id].append(item[:3])
                else:
                    operation_dict[row_id].append(item[:3])
            else:
                return Result(-1, ("unknown label: " + str(item)))

    anatomy_s, symptom_s, independent_s, drugs_s, operation_s, overall_s = 0, 0, 0, 0, 0, 0
    anatomy_r, symptom_r, independent_r, drugs_r, operation_r, overall_r = 0, 0, 0, 0, 0, 0
    predict, anatomy_body, symptom_body, independent_body, drugs_body, operation_body = 0, 0, 0, 0, 0, 0

    for row_id in dict_sub:
        if row_id not in dict_res:
            return Result(-1, ("unknown id:" + row_id))
        s_lst = dict_sub[row_id].split(';')[:-1]
        predict += len(s_lst)
        for item in s_lst:
            item = item.split('\t')
            if len(item) != 4:
                return Result(-1, ("incorrect format around id: " + str(row_id)))
            if item[3] == '解剖部位':
                anatomy_body += 1
                if row_id not in anatomy_dict:
                    continue
                if item[:3] in anatomy_dict[row_id]:
                    anatomy_s += 1
                    overall_s += 1
                    anatomy_r += 1
                    overall_r += 1
                    anatomy_dict[row_id].remove(item[:3])
                else:
                    for gold in anatomy_dict[row_id]:
                        if max(int(item[1]), int(gold[1])) <= min(int(item[2]), int(gold[2])):
                            anatomy_dict[row_id].remove(gold)
                            anatomy_r += 1
                            overall_r += 1
                            break
            elif item[3] == '症状描述':
                symptom_body += 1
                if row_id not in symptom_dict:
                    continue
                if item[:3] in symptom_dict[row_id]:
                    symptom_s += 1
                    overall_s += 1
                    symptom_r += 1
                    overall_r += 1
                    symptom_dict[row_id].remove(item[:3])
                else:
                    for gold in symptom_dict[row_id]:
                        if max(int(item[1]), int(gold[1])) <= min(int(item[2]), int(gold[2])):
                            symptom_dict[row_id].remove(gold)
                            symptom_r += 1
                            overall_r += 1
                            break
            elif item[3] == '独立症状':
                independent_body += 1
                if row_id not in independent_dict:
                    continue
                if item[:3] in independent_dict[row_id]:
                    independent_dict[row_id].remove(item[:3])
                    independent_s += 1
                    overall_s += 1
                    independent_r += 1
                    overall_r += 1
                else:
                    for gold in independent_dict[row_id]:
                        if max(int(item[1]), int(gold[1])) <= min(int(item[2]), int(gold[2])):
                            independent_dict[row_id].remove(gold)
                            independent_r += 1
                            overall_r += 1
                            break
            elif item[3] == '药物':
                drugs_body += 1
                if row_id not in drugs_dict:
                    continue
                if item[:3] in drugs_dict[row_id]:
                    drugs_dict[row_id].remove(item[:3])
                    drugs_s += 1
                    overall_s += 1
                    drugs_r += 1
                    overall_r += 1
                else:
                    for gold in drugs_dict[row_id]:
                        if max(int(item[1]), int(gold[1])) <= min(int(item[2]), int(gold[2])):
                            drugs_dict[row_id].remove(gold)
                            drugs_r += 1
                            overall_r += 1
                            break
            elif item[3] == '手术':
                operation_body += 1
                if row_id not in operation_dict:
                    continue
                if item[:3] in operation_dict[row_id]:
                    operation_dict[row_id].remove(item[:3])
                    operation_s += 1
                    overall_s += 1
                    operation_r += 1
                    overall_r += 1
                else:
                    for gold in operation_dict[row_id]:
                        if max(int(item[1]), int(gold[1])) <= min(int(item[2]), int(gold[2])):
                            operation_dict[row_id].remove(gold)
                            operation_r += 1
                            overall_r += 1
                            break
            else:
                return Result(-1, ("unknown label: " + str(item)))

    precision, recall, f1 = {}, {}, {},

    if anatomy_body == 0:
        precision['anatomy_s'] = 0
    else:
        precision['anatomy_s'] = anatomy_s / anatomy_body
    if symptom_body == 0:
        precision['symptom_s'] = 0
    else:
        precision['symptom_s'] = symptom_s / symptom_body
    if independent_body == 0:
        precision['independent_s'] = 0
    else:
        precision['independent_s'] = independent_s / independent_body
    if drugs_body == 0:
        precision['drugs_s'] = 0
    else:
        precision['drugs_s'] = drugs_s / drugs_body
    if operation_body == 0:
        precision['operation_s'] = 0
    else:
        precision['operation_s'] = operation_s / operation_body
    if predict == 0:
        precision['overall_s'] = 0
    else:
        precision['overall_s'] = overall_s / predict
    if anatomy_body == 0:
        precision['anatomy_r'] = 0
    else:
        precision['anatomy_r'] = anatomy_r / anatomy_body
    if symptom_body == 0:
        precision['symptom_r'] = 0
    else:
        precision['symptom_r'] = symptom_r / symptom_body
    if independent_body == 0:
        precision['independent_r'] = 0
    else:
        precision['independent_r'] = independent_r / independent_body
    if drugs_body == 0:
        precision['drugs_r'] = 0
    else:
        precision['drugs_r'] = drugs_r / drugs_body
    if operation_body == 0:
        precision['operation_r'] = 0
    else:
        precision['operation_r'] = operation_r / operation_body
    if predict == 0:
        precision['overall_r'] = 0
    else:
        precision['overall_r'] = overall_r / predict
    recall['anatomy_s'] = anatomy_s / anatomy_g
    recall['symptom_s'] = symptom_s / symptom_g
    recall['independent_s'] = independent_s / independent_g
    recall['drugs_s'] = drugs_s / drugs_g
    recall['operation_s'] = operation_s / operation_g
    recall['overall_s'] = overall_s / overall_g
    recall['anatomy_r'] = anatomy_r / anatomy_g
    recall['symptom_r'] = symptom_r / symptom_g
    recall['independent_r'] = independent_r / independent_g
    recall['drugs_r'] = drugs_r / drugs_g
    recall['operation_r'] = operation_r / operation_g
    recall['overall_r'] = overall_r / overall_g

    for item in precision:
        f1[item] = 2 * precision[item] * recall[item] / (precision[item] + recall[item])             if (precision[item] + recall[item]) != 0 else 0

    anatomy_s = [precision['anatomy_s'], recall['anatomy_s'], f1['anatomy_s']]
    anatomy_r = [precision['anatomy_r'], recall['anatomy_r'], f1['anatomy_r']]
    symptom_s = [precision['symptom_s'], recall['symptom_s'], f1['symptom_s']]
    symptom_r = [precision['symptom_r'], recall['symptom_r'], f1['symptom_r']]
    independent_s = [precision['independent_s'], recall['independent_s'], f1['independent_s']]
    independent_r = [precision['independent_r'], recall['independent_r'], f1['independent_r']]
    drugs_s = [precision['drugs_s'], recall['drugs_s'], f1['drugs_s']]
    drugs_r = [precision['drugs_r'], recall['drugs_r'], f1['drugs_r']]
    operation_s = [precision['operation_s'], recall['operation_s'], f1['operation_s']]
    operation_r = [precision['operation_r'], recall['operation_r'], f1['operation_r']]
    overall_r = [precision['overall_r'], recall['overall_r'], f1['overall_r']]
    overall_s = [precision['overall_s'], recall['overall_s'], f1['overall_s']]

    s = 'anatomy_s: ' + str(anatomy_s) + ' anatomy_r: ' + str(anatomy_r) + ' symptom_s: ' + str(symptom_s) + ' symptom_r: ' + str(symptom_r) + ' independent_s: ' + str(independent_s) + ' independent_r: ' + str(independent_r) + ' drugs_s: ' + str(drugs_s) + ' drugs_r: ' + str(drugs_r) + ' operation_s: ' + str(operation_s) + ' operation_r: ' + str(operation_r) + ' overall_r: ' + str(overall_r) + ' overall_s: ' + str(overall_s)

    return Result(f1['overall_s'], s)


# In[5]:

if __name__ == '__main__':
    print(ccks2018_1('89258.txt', 'ccks1_result400t.txt'))


# In[ ]:



