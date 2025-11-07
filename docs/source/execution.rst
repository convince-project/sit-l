Deploy model (if needed)
========================

Refer to `situation awareness VLM deployment <https://convince-project.github.io/sit-aw-aip/deploy_model.html>` 
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


Format data (if needed)
=======================

Refer to `situation awareness Format data <https://convince-project.github.io/sit-aw-aip/identification.html#format-data-generate-json-once-on-a-desired-batch-of-data>` 
section. It is the same command, as call it from there. 

Learning (inference)
====================

⚠ **The model will "learn" only if the identified anomaly is unknwon**

.. code-block:: bash

    learn \
    --use_case_id {id} \
    --anomaly_case_path {path} 

Refer to `situation awareness variables description <https://convince-project.github.io/sit-aw-aip/identification.html#id4>`
within the identification part. They represent the same. 
