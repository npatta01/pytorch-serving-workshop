cd /home/${NB_USER}

mkdir -p pytorch-serving-workshop

cd pytorch-serving-workshop
mkdir -p artifacts/dataset_processed/amazon
mkdir -p artifacts/dataset_processed/model


cd artifacts

BASE_URL="https://github.com/npatta01/pytorch-serving-workshop/releases/download/v0.0.1/"

# dataset
echo "downloading dataset"
wget --quiet "$BASE_URL/dataset_processed.zip"
unzip dataset_processed.zip


# model trained on above dataset
echo "downloading model"
wget --quiet "$BASE_URL/model.zip"
unzip model.zip