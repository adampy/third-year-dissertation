[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-7f7980b617ed060a017424585567c406b6ee15c891e84e1186181d67ecf80aa0.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=12899784)

# Directory explanation
- `/cluster-mgmt` - contains all required manifest and setup files to initialise the cluster. It also includes `installation_notes.md`, which was initially used to reference any guides used when installing the cluster. Setup files were used on the nodes in the cluster. This directory also contains the required TeaStore manifest, as well as a manifest defining the HPAs used in the experiments.
- `/cpas` - contains the manifest files for the PPAs, including a setup script, `setup.sh`, that is used to install the required resources, and initialise the PPAs.
- `/inference` - contains code required for the inference server, as well as a `Dockerfile` outlining the docker image used. It also contains `test.py` which was initially used to test the inference server was working correctly. `azure_blob.py` is used to interface with Azure Blob storage.
- `/limbo` - contains the require code and Docker image to run the load generator, LIMBO. It also contains all generated load profiles. It contains  a pyhton script called `timeseries_viewer.py` which was used to visualise load profiles.
- `/misc` - contains test manifests used for debugging the cluster, as well as examples for inputs and outputs of the PPAs.
- `/prometheus` - contains all results of every experiment, as well as a Python file to obtain data from Prometheus (`dataset_scraper.py`) and a Python file to evaluate the results once downloaded (`result_eval.py`). It also contains manifest files exposing Prometheus to external traffic, and allocating persistent volumes to Prometheus (the latter is required to allow Prometheus to run).

Anything in the root directory relates to the PPA itself. `metric.py` and `evaluate.py` both are part of the PPA, with `config.yaml` outlining the configuration of the PPA.

`ai.py`, however, is not used in the PPA but is used to train the ML models used in the PPAs.

# Load profiles of experiments
Below is a list of files used in each experiment. Load profiles were generated using `/limbo/simple_generate_load_profile.py` (and were generated using `/limbo/generate_load_profile.py` before using the `mockseries` library).

- Experiment 1 (high seasonality, high noise, no trend) - `/limbo/lp_b150_e150_s7200_r30_sa100_sp1800.csv`
- Experiment 2 (low seasonality, very low noise, trending) - `/limbo/lp_b150_e400_s7200_r5_sa15_sp300.csv`
- Experiment 3 (no seasonality, high noise) - `/limbo/lp_b250_e250_s1800_r30_sa0_sp300.cscv`

# Obtaining results
To obtain results from a Prometheus cluster, we ran the command `python prometheus/dataset_scraper.py` to download it. We had to modify the Python file's configuration (at the top of the file) to download appropriately. Once results were downloaded, we used `python prometheus/result_eval.py` to evaluate the results.