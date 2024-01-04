from statistics import mean
import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker
import inspect

'''
Organize simulation results from text file, plot graphs

'''

'''
results dictionary form

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







'''
ERROR GRAPHS
'''
# # LINE GRAPH 
# def plot_graphs(results):
#     plt.figure(figsize=(7, 6))
#     for category in results:
#         data = results[category]
#         computer_type = 'SLURM cluster with three workers'
#         sims_levels = sorted([sims_level for sims_level in data[computer_type].keys()])
#         average_errors = []
#         for sims_level in sims_levels:
#             average_error = 0
#             for computer_type in data:
#                 average_error += data[computer_type][sims_level]['average_error']
#             average_error /= len(list(data.keys()))
#             average_errors.append(average_error)
#         #average_errors = [data[computer_type][sims_level]['average_error'] for sims_level in sims_levels]
#         for i in range(len(sims_levels)):
#             sims_levels[i] = f"$10^{len(str(sims_levels[i]))-1}$"      
#         plt.plot(sims_levels, average_errors, label=category, linewidth=3)
#     plt.title(f'Monte Carlo European Call Option', fontsize=18)
#     plt.xlabel('Asset path simulations', fontsize=15)
#     plt.xticks(fontsize=12)
#     plt.yticks(fontsize=12)
#     plt.ylabel('Average error (USD)', fontsize=15)
#     plt.legend(fontsize=12)
#     plt.show()
# plot_graphs(results)



'''
RUNTIME GRAPHS
'''

# BAR CHART
# def plot_graphs(results):
#     width = 1/len(list(results['ATM'].keys()))  # Width of the bars in the bar chart
#     for category in results:
#         plt.figure(figsize=(7, 6))
#         data = results[category]
#         index = 0  # To keep track of which computer_type we are plotting
#         for computer_type in reversed(data):
#             sims_levels = sorted([sims_level for sims_level in data[computer_type].keys()])
#             average_runtimes = [data[computer_type][sims_level]['average_runtime'] for sims_level in sims_levels]
#             positions = [x + index * width for x in range(len(sims_levels))]
#             plt.bar(positions, average_runtimes, width, label=computer_type)
#             index += 1
#         for i in range(len(sims_levels)):
#             sims_levels[i] = f"$10^{len(str(sims_levels[i]))-1}$"
#         plt.xticks([r + width for r in range(len(sims_levels))], sims_levels)   
#         plt.title(f'{category} European Call Option')
#         plt.xlabel('Asset path simulations')
#         plt.ylabel('Average runtime (seconds)')
#         plt.legend()
#         plt.show()
# plot_graphs(results)

# LINE GRAPH WITH FILL UNDER LINE
# def plot_graphs(results):
#     for category in results:
#         plt.figure(figsize=(7, 6))
#         data = results[category]
#         for computer_type in data:
#             sims_levels = sorted([sims_level for sims_level in data[computer_type].keys()])            
#             average_runtimes = [data[computer_type][sims_level]['average_runtime'] for sims_level in sims_levels]
#             for i in range(len(sims_levels)):
#                 sims_levels[i] = f"$10^{len(str(sims_levels[i]))-1}$"
#             # Plotting the line
#             plt.plot(sims_levels, average_runtimes, label=computer_type)
#             # Filling the area under the curve
#             plt.fill_between(sims_levels, average_runtimes, alpha=.9)  # Adjust alpha for transparency
#         plt.yscale('log')  # Set y-axis to logarithmic scale
#         plt.title(f'{category} European Call Option')
#         plt.xlabel('Asset path simulations')
#         plt.ylabel('Average runtime (seconds)')
#         plt.legend()
#         plt.show()
# plot_graphs(results)
            
# LINE GRAPH 
def plot_graphs(results):
    for category in results:
        plt.figure(figsize=(7, 6))
        data = results[category]
        for computer_type in data:
            sims_levels = sorted([sims_level for sims_level in data[computer_type].keys()])            
            average_runtimes = [data[computer_type][sims_level]['average_runtime'] for sims_level in sims_levels]
            for i in range(len(sims_levels)):
                sims_levels[i] = f"$10^{len(str(sims_levels[i]))-1}$"      
            plt.plot(sims_levels, average_runtimes, label=computer_type, linewidth=3)
        plt.title(f'Monte Carlo {category} European Call Option', fontsize=18)
        plt.xlabel('Asset path simulations', fontsize=15)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.ylabel('Average runtime (seconds)', fontsize=15)
        plt.legend(fontsize=12)
        plt.show()
plot_graphs(results)

# LINE GRAPH LOG SCALE
def plot_graphs(results):
    for category in results:
        plt.figure(figsize=(7, 6))
        data = results[category]
        for computer_type in data:
            sims_levels = sorted([sims_level for sims_level in data[computer_type].keys()])            
            average_runtimes = [data[computer_type][sims_level]['average_runtime'] for sims_level in sims_levels]
            for i in range(len(sims_levels)):
                sims_levels[i] = f"$10^{len(str(sims_levels[i]))-1}$"      
            plt.plot(sims_levels, average_runtimes, label=computer_type, linewidth=3)
        plt.title(f'Monte Carlo {category} European Call Option', fontsize=18)
        plt.xlabel('Asset path simulations', fontsize=15)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.yscale('log')
        plt.ylabel('Average runtime (seconds)', fontsize=15)
        plt.legend(fontsize=12)
        plt.show()
plot_graphs(results)




