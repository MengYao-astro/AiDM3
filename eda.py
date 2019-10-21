import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
from math import log10, floor, ceil
from scipy.stats import norm
from matplotlib.patches import Rectangle

# Load IDs of page link origins and targets in new encoding
ID_From = np.load('ID_From.npy')
ID_To = np.load('ID_To.npy')

# Find unique page IDs (sequential under new encoding)
ID_Unique = np.unique(np.concatenate((ID_From, ID_To), axis=0))

# Count nonzero outgoing and incoming links
ID_Outgoing = np.zeros(len(ID_Unique))
ID_Incoming = np.zeros(len(ID_Unique))
ID_Outgoing_Nonzero, ID_Outgoing_Count = np.unique(ID_From, return_counts=True)
ID_Incoming_Nonzero, ID_Incoming_Count = np.unique(ID_To, return_counts=True)

# Find Dead ends and unlinked-pages
Dead_Ends = np.setdiff1d(ID_Unique, ID_Outgoing_Nonzero)
Unlinked = np.setdiff1d(ID_Unique, ID_Incoming_Nonzero)
print('There are', len(Dead_Ends), 'dead ends (without outgoing links).')
print('There are', len(Unlinked), 'pages without incoming links.')

# Plot histogram of incoming and outgoing link counts per page
Out_Hist = np.concatenate((np.zeros(len(Dead_Ends)), ID_Outgoing_Count), axis=0)
In_Hist = np.concatenate((np.zeros(len(Unlinked)), ID_Incoming_Count), axis=0)

# There are a lot of low link count pages so logscale is convenient
min_out, max_out = 0, 10**ceil(log10(np.max(Out_Hist)))
min_in, max_in = 0, 10**ceil(log10(np.max(In_Hist)))
bins_out = np.unique(np.insert(np.logspace(0., log10(max_out), num=20).astype(int), 0, 0))
bins_in = np.unique(np.insert(np.logspace(0., log10(max_in), num=20).astype(int), 0, 0))

# Set up plot for outgoing links
fig = plt.figure(dpi=plt.rcParams['figure.dpi']*4.0)
ax = fig.add_subplot(1, 1, 1)
plt.title('Outgoing Link Count Distribution (Logscale)')
plt.ylabel('Number of Pages')
plt.xlabel('Outgoing Links per Page (Average ~ ' + str(np.round(np.mean(Out_Hist),6)) + ')')
N, bins, patches = plt.hist(Out_Hist, range=(min_out, max_out), bins=bins_out, color='b')
patches[0].set_facecolor('r')
plt.yscale('log')
plt.xscale('log')
label = str(len(Dead_Ends)) + ' Dead Ends'
plt.legend([Rectangle((0,0),1,1,color='r') ], [label])
plt.savefig('out_hist.png', bbox_inches='tight')

# Set up plot for incoming links
plt.clf()
plt.title('Incoming Link Count Distribution (Logscale)')
plt.ylabel('Number of Pages')
plt.xlabel('Incoming Links per Page (Average ~ ' + str(np.round(np.mean(In_Hist),6)) + ')')
N, bins, patches = plt.hist(In_Hist, range=(min_in, max_in), bins=bins_in, color='b')
patches[0].set_facecolor('r')
plt.yscale('log')
plt.xscale('log')
label = str(len(Unlinked)) + ' Unlinked Pages'
plt.legend([Rectangle((0,0),1,1,color='r') ], [label])
plt.savefig('in_hist.png', bbox_inches='tight')

# Calculate average out-degree and in-degree
print('The average out-degree is', np.mean(Out_Hist))
print('The average in-degree is', np.mean(In_Hist))