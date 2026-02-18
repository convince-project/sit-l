Deploy model (if needed) or use the local version
=================================================

Refer to `situation awareness`_ VLM deployment section, if you want to deploy a model.

Installations
=============

Clone project
-------------

.. code-block:: bash

    git clone https://github.com/convince-project/sit-l.git

Build your project - Once
-------------------------

.. code-block:: bash 

    uv sync 

Activate virtual env - everytime you enter the project
------------------------------------------------------

.. code-block:: bash

    source .venv/bin/activate

Change environment variables (if you use a hosted model on a server)
--------------------------------------------------------------------

You will have to change the variables within *.env* to match the one defined when deploying the model.

**SERVER_IP** need to be the address of the serving hosting the model, else it will consider localhost by default. 

**Model** is the model you have chosen to deploy.

**PORT** is the port exposed by docker that you defined when deploying.

Same procedure as in situation awareness package.

Format data (if needed)
=======================

Refer to `situation awareness`_  Format data section. You can use the same command from this package than from the situation awareness package. 

Learning (inference)
====================

⚠ **The model will "learn" only if the identified anomaly is unknown**

.. code-block:: bash

    learn \
    --use_case_id {id} \
    --anomaly_case_path {path} \
    --local_model (optinal - default=False)

Refer to `situation awareness`_ variables description within the identification part. They represent the same. Apart from *local_model* variable : if you want the quantized local model, define this value as True.

.. _situation awareness : https://github.com/convince-project/sit-aw-aip

Customize to your use case 
==========================

1. Add your prompts to **convincesitl_mllm/prompts**, following the convention **prompt_UC{id}**. The id being the value that will point to your use case when executing the inference and data formatting.

2. Add your id and related values to the mapping, in the script **convincesitl_mllm/prompts/prompt_mapping.py**.
