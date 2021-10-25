import json
import logging
import os
import time
from abc import ABC
from collections.abc import Iterable
import transformers
import ast
import torch

import numpy as np
from ts.metrics.dimension import Dimension

logger = logging.getLogger(__name__)

from ts.torch_handler.base_handler import BaseHandler
from captum.attr import LayerIntegratedGradients

from ts.utils.util import map_class_to_label

import time


logger = logging.getLogger(__name__)
logger.info("Transformers version %s",transformers.__version__)

class CustomHandler(BaseHandler, ABC):
    """
    Transformers handler class for sequence classification.
    """

    def __init__(self):
        super(CustomHandler, self).__init__()
        self.initialized = False

    def initialize(self, ctx):

        
        self.manifest = ctx.manifest
        properties = ctx.system_properties
        model_dir = properties.get("model_dir")
        serialized_file = self.manifest["model"]["serializedFile"]
        model_pt_path = os.path.join(model_dir, serialized_file)

        self.device = torch.device(
            "cuda:" + str(properties.get("gpu_id"))
            if torch.cuda.is_available() and properties.get("gpu_id") is not None
            else "cpu"
        )
        
        # read configs for the mode, model_name, etc. from setup_config.json
        setup_config_path = os.path.join(model_dir, "setup_config.json")
        if os.path.isfile(setup_config_path):
            with open(setup_config_path) as setup_config_file:
                self.setup_config = json.load(setup_config_file)
        else:
            logger.warning("Missing the setup_config.json file.")


        # Loading the model and tokenizer from checkpoint and config files based on the user's choice of mode
        # further setup config can be added.
        if self.setup_config["save_mode"] == "jit":
            self.model = torch.jit.load(model_pt_path, map_location=self.device)
        elif self.setup_config["save_mode"] == "original":
            self.model = transformers.AutoModelForSequenceClassification.from_pretrained(model_dir)

            self.model.to(self.device)
            
        else:
            logger.warning("Missing the checkpoint or state_dict.")

            
        
        self.top_k = self.setup_config["top_k"]
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(model_dir 
                                                                    , do_lower_case=self.setup_config["do_lower_case"]
                                                                    , torchscript=True)

      
        self.model.eval()

        logger.info(
            "Transformer model from path %s loaded successfully", model_dir
        )

        # Read the mapping file, index to object name
        mapping_file_path = os.path.join(model_dir, "index_to_name.json")
        
        if os.path.isfile(mapping_file_path):
            with open(mapping_file_path) as f:
                self.mapping = json.load(f)
        else:
            logger.warning("Missing the index_to_name.json file.")
        
        self.initialized = True

    def preprocess(self, requests):
        """Basic text preprocessing, based on the user's chocie of application mode.
        Args:
            requests (str): The Input data in the form of text is passed on to the preprocess
            function.
        Returns:
            list : The preprocess function returns a list of Tensor for the size of the word tokens.
        """
        input_ids_batch = None
        attention_mask_batch = None
        for idx, data in enumerate(requests):
            request = data.get("data")
            if request is None:
                request = data.get("body")
            if isinstance(request, (bytes, bytearray)):
                request = request.decode('utf-8')

            input_text = request['text']
            max_length = self.setup_config["max_length"]
            logger.info("Received text: '%s'", input_text)

            # preprocessing text for sequence_classification and token_classification.
            inputs = self.tokenizer.encode_plus(input_text, max_length=int(max_length), pad_to_max_length=True, add_special_tokens=True, return_tensors='pt')
            
            
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)
            # making a batch out of the recieved requests
            # attention masks are passed for cases where input tokens are padded.
            if input_ids.shape is not None:
                if input_ids_batch is None:
                    input_ids_batch = input_ids
                    attention_mask_batch = attention_mask
                else:
                    input_ids_batch = torch.cat((input_ids_batch, input_ids), 0)
                    attention_mask_batch = torch.cat((attention_mask_batch, attention_mask), 0)
        
        input_ids_batch = input_ids_batch.to(self.device)
        attention_mask_batch = attention_mask_batch.to(self.device)
        
        return (input_ids_batch, attention_mask_batch)

    def inference(self, input_batch):

        
        input_ids_batch, attention_mask_batch = input_batch
        inferences = []
        
        predictions = self.model(input_ids_batch, attention_mask_batch)
        
#         ps = torch.nn.functional.softmax(predictions.logits, dim=1)
#         probs, classes = torch.topk(ps, self.top_k, dim=1)
#         probs = probs.tolist()
#         classes = classes.tolist()

#         inferences = map_class_to_label(probs, self.mapping, classes)
        
        num_rows, num_cols = predictions[0].shape
        for i in range(num_rows):
            ps = torch.nn.functional.softmax(predictions[i], dim=1)
            probs, classes = torch.topk(ps, self.top_k, dim=1)
            probs = probs.tolist()
            classes = classes.tolist()
        
            friendly_labels = map_class_to_label(probs, self.mapping, classes)
            inferences.append(friendly_labels)


        return inferences

    def postprocess(self, inference_output):

        return inference_output
   
    
    def handle(self, data, context):

        # It can be used for pre or post processing if needed as additional request
        # information is available in context
        
        start_time = time.time()
        
        self.context = context
        metrics = self.context.metrics
        
        data_preprocess = self.preprocess(data)
        data_inference = self.inference(data_preprocess)
        data_postprocess = self.postprocess(data_inference)
        
        
        
        stop_time = time.time()
        metrics.add_time('HandlerTime', round((stop_time - start_time) * 1000, 2), None, 'ms')
        
        return data_postprocess