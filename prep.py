import numpy as np

# Load IDs of page link origins and targets
file_name = 'wikilink_graph.2004-03-01.csv'
ID_From = np.genfromtxt(file_name, delimiter='\t', usecols= 0, dtype=np.int32, skip_header=1)
ID_To = np.genfromtxt(file_name, delimiter='\t', usecols= 2, dtype=np.int32, skip_header=1)

# Make list of all pages. Ordered indices are the new IDs/coding.
ID_Values, ID_Indices = np.unique(np.concatenate((ID_From, ID_To), axis=0), return_inverse=True)

# Replace old linking columns with new IDs
ID_From_New, ID_To_New = ID_Indices[0:len(ID_From)], ID_Indices[len(ID_From):len(ID_Indices)]

# Save columns
np.save('ID_From.npy', ID_From_New)
np.save('ID_To.npy', ID_To_New)