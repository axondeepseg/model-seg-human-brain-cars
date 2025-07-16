# model-seg-human-brain-cars
Axon and myelin segmentation model in histology images to quantify myelination in the human brain. Training data was acquired in the uncinate fasciulus using CARS microscopy.

## How to use
To use this segmentation model in AxonDeepSeg, simply download it from the latest release ([here](https://github.com/axondeepseg/model-seg-human-brain-cars/releases/download/r20250716/model_seg_axon_myelin_human_exvivo_cars.zip)), decompress it and place it under your `AxonDeepSeg/models` folder. Then, you can use the model with AxonDeepSeg:
```bash
> axondeepseg -i [PATH_TO_INPUT] -m [PATH_TO_MODEL_FOLDER]
```
