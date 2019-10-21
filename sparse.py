import numpy as np
from scipy.sparse import csc_matrix

# Load IDs of page link origins and targets and all unqiue IDS
ID_From = np.load('ID_From.npy')
ID_To = np.load('ID_To.npy')

# Find unique page IDs
# These pages will be both the rows and columns of our matrix M
ID_Unique = np.unique(np.concatenate((ID_From, ID_To), axis=0))

# Count nonzero outgoing links
# This will serve as the denominator for the columns of our matrix M
# ie, assuming even probability 1 / (the total outgoing count) is the 
# proability of going to the page of a row from the page of a column
ID_Outgoing_Nonzero, ID_Outgoing_Count = np.unique(ID_From, return_counts=True)

# Create our matrix
M = csc_matrix((np.ones(len(ID_From)), (ID_To, ID_From)), shape=(len(ID_Unique), len(ID_Unique)))

# Normalize dividing columns by total count 
# Will use 1 if dead end - will still be 0 - no entry in sparse - but avoids nans
Norm = np.ones(len(ID_Unique))
Norm[ID_Outgoing_Nonzero] = ID_Outgoing_Count
val = np.repeat(Norm, M.getnnz(axis=0)) # This keeps the sparse matrix a sparse matrix
M.data /= val

# Create v with even inital distribution
v = np.ones(len(ID_Unique))
v /= len(ID_Unique)

# Iterate to create vNew
beta = 0.8