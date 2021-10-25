# Readme


## Overview


This repo contains notebooks for Pytorch Serving Workshop.


To get started, run the below notebook that will setup everything in collab. 

**Colab** starter notebook: &nbsp;&nbsp; [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/npatta01/pytorch-serving-workshop/blob/main/colab_starter.ipynb)


## Contents

There are five notebooks.

a. 00_prepare_dataset.ipynb

Notebook that prepares the e-comeerce dataset and saves it.

b. 01_train.ipynb

Trains a DistilBert model

c. 02_inference_review.ipynb

Notebook that shows how to use the HuggingFace ecosystem. Also shows how to use the trained model from previous notebook.

d. 03_optimizing_model.ipynb

Notebook that shows impact of Quantization and TorschScript


e. 04_packaging.ipynb

Notebook that shows how to use TorchServe to serve models


## References

[Pydata 2021 Slides](https://docs.google.com/presentation/d/1NF7_vZgGVYM4G-YHcfWIru56FwzycV04QjILEBjjJZM/edit?usp=sharing)

[Pydata 2021 Conference Page](https://pydata.org/global2021/schedule/presentation/136/serving-pytorch-models-in-production/)


## Libraries

This repro uses HuggingFace transformers and dataset pacakge. 

The dataset used is [Amazon Berkeley Objects (ABO) Dataset](https://amazon-berkeley-objects.s3.amazonaws.com/index.html) created by Amazon and UC Berkeley.
For more reference, refer to this [paper](https://arxiv.org/abs/2110.06199)


## Contact

For help or feedback, please reach out to [Nidhin Pattaniyil](https://www.linkedin.com/in/nidhinpattaniyil/) or [Adway Dhillon](https://www.linkedin.com/in/adwaydhillon/)
