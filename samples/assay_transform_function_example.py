# Import the transform helper from the labkey python api library
from labkey.utils import transform_helper

# the run properties filepath must be defined in this way so that it can be fed into the transform helper
filepath = '${runInfo}'

# define the function that you are using to transform your results data array
def transform(grid):
    isHeaderChecked = False    
    # iterate through the rows of your results data, checking for the header
    for row in grid:
        if isHeaderChecked == False:
            row.append('averageResult')
            isHeaderChecked = True
        else:
            # In this example, we are taking the average of the 3rd-5th column values by row and appending that average value in a 6th column called "averageResult"
            newValTemp = sum([float(val) for val in row[2:]])/len(row[2:])
            row.append(round(newValTemp, 2))
    return grid

#call the transform helper using your user-defined transform function and the run properties filepath
transform_helper(transform, filepath)
