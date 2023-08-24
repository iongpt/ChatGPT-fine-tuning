---

# ChatGPT 3.5 Fine-tuning Utilities

This project provides a set of utilities to assist users in fine-tuning the ChatGPT 3.5 model with OpenAI. 
The utilities are wrapped into a single `TrainGPT` class which allows users to manage the entire fine-tuning lifecycle - from uploading data files, to starting training jobs, monitoring their progress, and managing the trained models.

## Features:

- **File Upload**: Easily upload your fine-tuning data files.
- **Start Training**: Begin a new training job using your uploaded data.
- **List Jobs**: View all your current and past training jobs.
- **Job Details**: Retrieve detailed information about a specific training job.
- **Cancel**: Cancel a training job.
- **Delete**: Delete a training job.
- **List Models**: View all your current and past fine-tuned models.
- **Model Details**: Retrieve detailed information about a specific model.
- **Delete Model**: Delete a fine-tuned model.
---

## Prerequisites:

- **API Key**: Ensure you have set up your OpenAI API key. You can set it as an environment variable named `OPENAI_API_KEY`.

```angular2html
export OPENAI_API_KEY="your_api_key"
```

## Installation:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your_username/chatgpt-fine-tuning-utilities.git
   cd chatgpt-fine-tuning-utilities
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Prepare your data:

Data needs to be in JSONL format:
```json
[
  {
  "messages": [
    { "role": "system", "content": "You are an assistant that occasionally misspells words" },
    { "role": "user", "content": "Tell me a story." },
    { "role": "assistant", "content": "One day a student went to schoool." }
  ]
},
  {
  "messages": [
    { "role": "system", "content": "You are an assistant that occasionally misspells words" },
    { "role": "user", "content": "Tell me a story." },
    { "role": "assistant", "content": "One day a student went to schoool." }
  ]
}
]
```
Save it as `data.jsonl` in the root directory of the project.


## Detailed Usage:

### **Python Script Usage**:

After setting up, you can utilize the `TrainGPT` class in your Python scripts as follows:

1. **Initialization**:

    Start by importing and initializing the `TrainGPT` class.

    ```python
    from train_gpt_utilities import TrainGPT
    trainer = TrainGPT()
    ```

2. **Upload Training Data**:

    Upload your training data file to start the fine-tuning process.

    ```python
    trainer.create_file("path/to/your/training_data.jsonl")
    ```

3. **Start a Training Job**:

    Begin the training process using the uploaded file.

    ```python
    trainer.start_training()
    ```

4. **Fetching Job Details**:

    You can get detailed statistics of a specific training job.

    ```python
    job_details = trainer.get_job_details("specific_job_id")
    ```

### **Command Line Usage**:

For those who prefer command-line tools, the provided CLI offers a straightforward way to manage the fine-tuning process.

1. **Uploading a File**:

    ```bash
    python train_gpt_cli.py --create-file /path/to/your/file.jsonl
    ```

2. **Starting a Training Job**:

    ```bash
    python train_gpt_cli.py --start-training
    ```

3. **Listing All Jobs**:

    ```bash
    python train_gpt_cli.py --list-jobs
    ```


For any command that requires a specific job or file ID, you can provide it as an argument. For example:

```bash
python train_gpt_cli.py --get-job-details your_job_id
```



## Contribution:

We welcome contributions to this project. If you find a bug or want to add a feature, feel free to open an issue or submit a pull request.

## License:

This project is licensed under the MIT License. See [LICENSE](./LICENSE) for more details.
