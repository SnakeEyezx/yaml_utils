from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
data = {}
yaml = YAML()
trace = []
# stack = 'C:\\Users\\Nitro\\PycharmProjects\\kafkadev\\venv\\level.yaml'
stack = 'C:\\Users\\Nitro\\PycharmProjects\\kafkadev\\venv\\labels.yml'

with open(stack, 'r') as stream:
    data = yaml.load(stream)

def recursive_printer(obj,level,key):
    for k, v in obj.items():
        if isinstance(v, CommentedMap):
            print(f'{level}{k}:')
            level += '  '
            recursive_printer(v, level,key)
            level = level.replace("  ", "", 1)
        else:
            if isinstance(v, list):
                print(f'{level}{k}:')
                for i in v:
                    print(f'{level}  - {i}')
            elif isinstance(v, (str,int)):
                print(f'{level}{k}: {v}')
            else:
                print('unknown type')



def recursive_search_v2(obj,key):
    if key in obj.keys():
        print(" >> ".join(s for s in trace))
        if isinstance(obj[key], CommentedMap):
            recursive_printer(obj[key],'  ',key)
        else:
            if isinstance(obj[key], CommentedSeq):
                print(f'{key}: ')
                for i in obj[key]:
                    print(f'  - {i}')
            elif isinstance(obj[key], (str,int)):
                print(f'{key}: {v}')
            else:
                print(trace)

    for k,v in obj.items():
        if isinstance(v, CommentedMap):
                trace.append(k)
                recursive_search_v2(v,key)
                trace.pop()

def recursive_search_value(obj, value):
    for k,v in obj.items():
        if isinstance(v,CommentedMap):
            trace.append(k)
            recursive_search_value(v,value)
            trace.pop()
        elif isinstance(v,CommentedSeq) and value in v:
            trace.append(k)
            print(" >> ".join(s for s in trace))
            print(v)
            trace.pop()


def change_value(obj,key,value):
    if key in obj.keys():
        print(" >> ".join(s for s in trace))
        target = obj[key]
        if isinstance(target, (str, int)):
            target = value
            print(target)
        elif isinstance(target, list):
            if value not in target:
                target.append(value)
            print(target)
        else:
            print('Error: unknown type')

    for k,v in obj.items():
        if isinstance(v, CommentedMap):
                trace.append(k)
                change_value(v,key,value)
                trace.pop()

test_list = []

def func_test_list(data):
    for k,v in data.items():
        test_list.append(k)
        if isinstance(v, CommentedMap):
            func_test_list(v)


def labels_diff(host):
    i = list(data['labels'][host])
    d = list(data['labels']['host2'])
    a = list(set(i).difference(set(d)))
    b = list(set(d).difference(set(i)))
    a.sort()
    b.sort()
    c = set(i).symmetric_difference(set(d))
    for h in a:
        print(f'+ {h}')
    for h in b:
        print(f'- {h}')


# list1: [1, 2, 5, 1, 3, 4, 10]
# {{ list1 | unique }}
# => [1, 2, 5, 3, 4, 10]

# list1: [1, 2, 5, 1, 3, 4, 10]
# list2: [1, 2, 3, 4, 5, 11, 99]
# {{ list1 | symmetric_difference(list2) }}
# => [10, 11, 99]


# recursive_printer(data, '')
# recursive_search_v2(data,'limits')
# recursive_search_v2(data,'preferences')
# change_value(data,'pids', '100M')
# recursive_search_value(data,'label-A=True')
labels_diff('host0')
# test
# TETS
# func_test_list(data)
# print(test_list)
# for i in test_list:
#     recursive_search_v2(data,i)
