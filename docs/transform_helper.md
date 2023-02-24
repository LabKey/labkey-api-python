# Transform Helper Function Support

This helper function provides a convenient way for users to write transform scripts for assays without requiring the user to read the results and run data before transforming the data, and it also takes care of writing the transformed data back to labkey.

### importing and preparing the helper function

First, your script must begin with these two lines to properly use the transform helper function:

```python
from labkey.utils import transform_helper

filepath = '${runInfo}'
```

The substitution token `${runInfo}` is replaced with the runProperties file path when the transform script is run within LabKey Server.

### Write your user-defined transform function

This is an example function that could be used as an argument when using the transform_helper function:

```python
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
```

As you can see in the example function, the transform function must accept only one argument, the tabular data (including headers) that needs to be transformed in an list of lists format. The user-defined transform function must also return tabular data the same list of lists format with a header row that matches the header of the results data as defined by the targeted assay design.

### using the helper function

The last thing to do is call the transform_helper function, supplying the user-defined transfrom function as the first argument, and the file path (as defined by ${runInfo}) as the second argument.

```python
transform_helper(transform, filepath)
``` 