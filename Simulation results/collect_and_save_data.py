from statistics import mean
import json
import pandas as pd

'''
Stores text file simulation results in a dictionary of the form:


results = {
    'OTM': {
        'single, independent computer': {
            'sims = 100': {
                'runtimes': [1.0, 2.0, 3.0],
                'prices': [1.0, 2.0, 3.0],
                'average_runtime': 2.0,
                'average_error': 1.0
            },
            'sims = 1000': {
                ...
            }
        },
        'nodes = 1': {
            ...
        }
    },
    'ITM': {
        ...
    },
    ...
}
'''

simulation_results = {'OTM':'OTM SIMULATION RESULTS wo head.txt', 
         'ITM':'ITM SIMULATION RESULTS wo head.txt', 
         'ATM': 'ATM SIMULATION RESULTS wo head.txt'}
BS_prices = {'OTM': 4.715052031,
        'ITM': 16.79983686,
        'ATM': 9.826297782 }
results = {'OTM': {}, 
           'ITM': {}, 
           'ATM': {}}

for option_type in simulation_results.keys():
    with open(simulation_results[option_type], 'r') as file: 
        current_computer_type = None
        current_sims = None
        for line in file:
            if 'single, independent computer' in line or 'nodes =' in line:
                current_computer_type = line.strip()
                if current_computer_type == 'nodes = 1':
                    current_computer_type = 'SLURM cluster with one worker'
                elif current_computer_type == 'nodes = 2':
                    current_computer_type = 'SLURM cluster with two workers'
                elif current_computer_type == 'nodes = 3':
                    current_computer_type = 'SLURM cluster with three workers'
                elif current_computer_type == 'nodes = 4':
                    current_computer_type = 'SLURM cluster with four workers'
                if current_computer_type not in results[option_type].keys():
                    results[option_type][current_computer_type] = {}
            elif 'sims =' in line:
                current_sims = int(line.split('=')[1].strip())
                results[option_type][current_computer_type][current_sims] = {'runtimes': [], 'prices': []}
            elif 'run' in line and ',' in line and 'seconds' in line:
                parts = line.split(',')
                runtime = parts[1].split()[0].strip()
                results[option_type][current_computer_type][current_sims]['runtimes'].append(float(runtime))
            elif 'run' in line and ',' in line and 'seconds' not in line:
                parts = line.split(',')
                price = parts[1].split()[0].strip()
                results[option_type][current_computer_type][current_sims]['prices'].append(float(price))
    for computer_type in results[option_type].keys():
        for sims in results[option_type][computer_type].keys():
            results[option_type][computer_type][sims]['average_runtime'] = mean(results[option_type][computer_type][sims]['runtimes'])
            results[option_type][computer_type][sims]['average_error'] = mean([abs(x-BS_prices[option_type]) for x in results[option_type][computer_type][sims]['prices']])


# #put into excel format
# excel_writer = pd.ExcelWriter('simulation_results.xlsx', engine='xlsxwriter')
# for option_type in results.keys(): #runtimes
#     data = []
#     for simulation_level in results[option_type][list(results[option_type].keys())[0]].keys():
#         row = {'Simulation Level': simulation_level}
#         for computer_type in results[option_type].keys():
#             row[computer_type] = results[option_type][computer_type][simulation_level]['average_runtime']
#         data.append(row)
#     df = pd.DataFrame(data)
#     df.to_excel(excel_writer, sheet_name=f"{option_type} runtime", index=False)
# for option_type in results.keys(): #errors
#     data = []
#     for simulation_level in results[option_type][list(results[option_type].keys())[0]].keys():
#         row = {'Simulation Level': simulation_level}
#         for computer_type in results[option_type].keys():
#             row[computer_type] = results[option_type][computer_type][simulation_level]['average_error']
#         data.append(row)
#     df = pd.DataFrame(data)
#     df.to_excel(excel_writer, sheet_name=f"{option_type} error", index=False)    
# excel_writer.save() #save workbook

# #print all average runtimes and average errors
# for option_type in results.keys():
#     print('\n----------------')
#     print(option_type)
#     print('----------------')
#     print('AVERAGE RUNTIMES')
#     for computer_type in results[option_type].keys():
#         print(computer_type)
#         for sims in results[option_type][computer_type].keys():
#             print(sims, results[option_type][computer_type][sims]['average_runtime'])
#     print('\nAVERAGE ERRORS')
#     for computer_type in results[option_type].keys():
#         print(computer_type)
#         for sims in results[option_type][computer_type].keys():
#             print(sims, results[option_type][computer_type][sims]['average_error'])

# save to a file
file_path = 'simulation_results.json'
with open(file_path, 'w') as file:
    json.dump(results, file)

# with open(file_path, 'r') as file:
#     retrieved_results = json.load(file)

# print(retrieved_results == results)

