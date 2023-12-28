# LabKey Experiment API Overview

Load or save LabKey assay batches associated with existing assays/protocols.

An assay batch is a set of runs uploaded in a single session. Some properties in a design apply to entire batches of runs. This python API lets users retrieve batch data and save new batch data to their LabKey Server instance.

Learn more about assays here, https://www.labkey.org/Documentation/wiki-page.view?name=instrumentData.

### LabKey Experiment API Methods

To use the experiment API methods, you must first instantiate an APIWrapper object. See the APIWrapper docs page to learn more about how to properly do so, accounting for your LabKey Server's configuration details.

**load_batch**

List of method parameters:
- assay_id: The protocol id of the assay from which to load a batch.
- batch_id: The id of the batch being loaded.

**save_batch**

List of method parameters:
- assay_id: The assay protocol id.
- batch: The Batch to save.

**save_batches**

List of method parameters:
- assay_id: The assay protocol id.
- batches: The Batch(es) to save.
