# Normal PCB Image Sources

## 1. DeepPCB, recommended for main experiments

Source: https://github.com/tangsanli5201/DeepPCB

Local path:

```text
data/raw/deeppcb/DeepPCB/PCBData/
```

DeepPCB contains paired PCB images:

```text
*_temp.jpg  defect-free template image, can be used as normal PCB
*_test.jpg  tested image with defects
*.txt       defect bounding-box annotations
```

Local count:

```text
normal template images: 1501
defective/test images: 1500
```

Recommended use:

```text
Task 1: normal vs defect binary classification
normal = *_temp.jpg
defect = *_test.jpg

Task 2: six defect type classification
crop defect patches from *_test.jpg according to the annotation txt files
```

This is the most reliable source because normal and defective samples come from the same imaging pipeline.

## 2. AWS Lookout for Vision circuitboard, for demo/PPT only

Source: https://github.com/aws-samples/amazon-lookout-for-vision

Local path:

```text
data/raw/aws_circuitboard/circuitboard/
```

Local count:

```text
normal images: 40
anomaly images: 40
```

Recommended use:

```text
PPT visual examples
small normal/anomaly classification demo
```

Do not mix this dataset with DeepPCB or Kaggle PCB Defects for the main binary experiment unless explicitly discussing domain shift, because the board style, color, camera setup, and defect definition are different.

## 3. VisA PCB subsets, optional extension

Source: https://dagshub.com/datasets/visual-anomaly-visa/

VisA contains four PCB subsets, pcb1 to pcb4, with normal and anomalous samples. It is useful for assembled-board anomaly detection, but the anomaly labels are not the same as the six DeepPCB defect categories.

Recommended use:

```text
optional extension experiment
normal/anomaly detection on assembled PCB images
```
