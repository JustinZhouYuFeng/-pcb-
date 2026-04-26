# VisA PCB Dataset Notes

## Official sources

- AWS Open Data Registry: https://registry.opendata.aws/visa/
- GitHub project: https://github.com/amazon-science/spot-diff
- Paper: https://arxiv.org/abs/2207.14315

## Why VisA is suitable for this seminar

VisA is more suitable than DeepPCB for the main visual presentation because it
contains real-color PCB images. The PCB subsets include transistors, capacitors,
chips and other mounted components, so the images are closer to a practical
electronics inspection scenario.

## Dataset scale

The full VisA dataset contains:

```text
10,821 images
9,621 normal images
1,200 anomaly images
12 object subsets
```

PCB subsets:

```text
PCB1: 1,004 normal, 100 anomaly, 4 anomaly classes
PCB2: 1,001 normal, 100 anomaly, 4 anomaly classes
PCB3: 1,006 normal, 100 anomaly, 4 anomaly classes
PCB4: 1,005 normal, 100 anomaly, 7 anomaly classes
```

## Recommended use in this project

Main experiment:

```text
VisA pcb1-pcb4 normal/anomaly binary classification
```

Reason:

```text
The dataset has clean normal and anomalous labels.
It uses real-color PCB images.
It supports false positive and false negative analysis.
It also provides pixel-level masks for optional segmentation discussion.
```

Optional extension:

```text
Use DeepPCB for standard six-defect category recognition.
```

DeepPCB is useful for defect-type classification, but its binary/template-like
images are less visually realistic than VisA.
