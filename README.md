# PyTorch Serving Workshop


## Overview


This repository contains notebooks for a PyTorch model-serving workshop.

You **do not** need a GPU runtime.

## Setup 

During the workshop, use this custom [JupyterHub](http://hub2.np.training), which has all dependencies preinstalled.



Outside the workshop, use [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/npatta01/pytorch-serving-workshop/main).



## Contents

There are five notebooks.

a. `00_prepare_dataset.ipynb`

Prepares and saves the e-commerce dataset.

b. `01_train.ipynb`

Trains a DistilBERT model.

c. `02_inference_review.ipynb`

Introduces the Hugging Face ecosystem and shows how to use the trained model from the previous notebook.

d. `03_optimizing_model.ipynb`

Demonstrates the impact of quantization and TorchScript.


e. `04_packaging.ipynb`

Shows how to package and serve models with TorchServe.


## Slides

[![Watch the video](assets/slides_cover.png)](https://www.slideshare.net/nidhinpattaniyil/serving-bert-models-in-production-with-torchserve)


## Video

[![PyData Video](https://img.youtube.com/vi/sDGxzkOvxqY/0.jpg)](https://www.youtube.com/watch?v=sDGxzkOvxqY&ab_channel=PyData)


## References

[Pydata 2021 Slides](https://www.slideshare.net/nidhinpattaniyil/serving-bert-models-in-production-with-torchserve)

[Pydata 2021 Conference Page](https://pydata.org/global2021/schedule/presentation/136/serving-pytorch-models-in-production/)


## Libraries

This repository uses the Hugging Face Transformers and Datasets packages.

The dataset used is [Amazon Berkeley Objects (ABO) Dataset](https://amazon-berkeley-objects.s3.amazonaws.com/index.html) created by Amazon and UC Berkeley.
For more information, see the accompanying [paper](https://arxiv.org/abs/2110.06199).


## Contact

For help or feedback, please reach out to:

- [Nidhin Pattaniyil](https://www.linkedin.com/in/nidhinpattaniyil/)   
- [Adway Dhillon](https://www.linkedin.com/in/adwaydhillon/)    
- [Vishal Rathi](https://www.linkedin.com/in/vishalkumarrathi/)   
