Deploy model (if needed)
========================

Refer to `situation awareness VLM deployment`_ 
section. 

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

Change environment variables
""""""""""""""""""""""""""""

You will have to change the variables within *.env* to match the one defined when deploying
the model.

**SERVER_IP** need to be the address of the serving hosting the model, else it will consider 
localhost by default. 

**Model** is the model you have chosen to deploy.

**PORT** is the port exposed by docker that you defined when deploying.

Same procedure as in situation awareness package.

Format data (if needed)
=======================

Refer to `situation awareness Format data`_ 
section. It is the same command, as call it from there. 

Learning (inference)
====================

⚠ **The model will "learn" only if the identified anomaly is unknwon**

.. code-block:: bash

    learn \
    --use_case_id {id} \
    --anomaly_case_path {path} 

Refer to `situation awareness variables description`_
within the identification part. They represent the same. 

.. _situation awareness VLM deployment: <https://convince-project.github.io/sit-aw-aip/deploy_model.html>
.. _situation awareness Format data: <https://convince-project.github.io/sit-aw-aip/identification.html#format-data-generate-json-once-on-a-desired-batch-of-data>
.. _situation awareness variables description: <https://convince-project.github.io/sit-aw-aip/identification.html#id4>
