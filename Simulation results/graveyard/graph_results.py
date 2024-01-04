import json
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker



file_path = 'simulation_results.json'
with open(file_path, 'r') as file:
    results = json.load(file)












# def plot_graphs(results):
#     for category in results:
#         plt.figure(figsize=(8, 6))
#         data = results[category]
#         for computer_type in data:
#             sims_levels = sorted([int(sims_level) for sims_level in data[computer_type].keys()])
#             average_runtimes = [data[computer_type][str(sims_level)]['average_runtime'] for sims_level in sims_levels]
#             plt.plot(sims_levels, average_runtimes, label=computer_type)
        
#         plt.xscale('log')
#         plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'$10^{{{int(np.log10(x))}}}$'))
#         plt.xticks(sims_levels, rotation=45)
#         plt.title(f'{category} European Call Option')
#         plt.xlabel('No. simulations')
#         plt.ylabel('Average runtime (seconds)')
#         plt.legend()
#         plt.show()

# plot_graphs(results)






# def plot_graphs(results):
#     for category in results:
#         plt.figure(figsize=(6, 4))
#         data = results[category]
#         for computer_type in data:
#             sims_levels = list(data[computer_type].keys())
#             average_runtimes = [data[computer_type][sims_level]['average_runtime'] for sims_level in sims_levels]
#             plt.plot(sims_levels, average_runtimes, label=computer_type)
        
#         plt.xticks(rotation=45)
#         plt.title(f'{category} European Call Option')
#         plt.xlabel('No. simulations')
#         plt.ylabel('Average runtime (seconds)')
#         plt.legend()
#         plt.show()

# plot_graphs(results)


