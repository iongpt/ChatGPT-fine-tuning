from datetime import datetime
import os

import openai
import argparse


def format_jobs_output(jobs_data):
    # Extract the list of jobs from the data
    jobs = jobs_data["data"]

    # Initialize counters
    total_jobs = len(jobs)
    job_type_count = {}
    status_count = {}

    # Iterate over jobs to populate counters
    for job in jobs:
        # Count job types
        job_type = job["object"]
        job_type_count[job_type] = job_type_count.get(job_type, 0) + 1

        # Count job statuses
        status = job["status"]
        status_count[status] = status_count.get(status, 0) + 1

    # Start building the output
    output = []

    # Add total job count
    output.append(f"There are {total_jobs} jobs in total.")

    # Add job type counts
    for job_type, count in job_type_count.items():
        output.append(f"{count} jobs of {job_type}.")

    # Add status counts
    for status, count in status_count.items():
        output.append(f"{count} jobs {status}.")

    # Add individual job details
    output.append("\nList of jobs (ordered by creation date):")
    for job in sorted(jobs, key=lambda x: x["created_at"]):
        created_at = datetime.utcfromtimestamp(job["created_at"]).strftime('%Y-%m-%d %H:%M:%S')
        finished_at = datetime.utcfromtimestamp(job["finished_at"]).strftime('%Y-%m-%d %H:%M:%S') if job[
            "finished_at"] else None
        output.append(f"""
- Job Type: {job["object"]}
  ID: {job["id"]}
  Model: {job["model"]}
  Created At: {created_at}
  Finished At: {finished_at}
  Fine Tuned Model: {job["fine_tuned_model"]}
  Status: {job["status"]}
  Training File: {job["training_file"]}
        """)

    return "\n".join(output)


class TrainGPT:
    def __init__(self, api_key=None, model_name="gpt-3.5-turbo"):
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key is None:
                raise ValueError("OPENAI_API_KEY environment variable is not set")

        openai.api_key = api_key
        self.model_name = model_name
        self.file_id = None
        self.job_id = None
        self.model_id = None

    def create_file(self, file_path):
        file = openai.File.create(
            file=open(file_path, "rb"),
            purpose='fine-tune'
        )
        self.file_id = file.id
        print(f"File ID: {self.file_id}")

    def start_training(self, file_id=None):
        if file_id is None:
            file_id = self.file_id

        if file_id is None:
            raise ValueError("File not uploaded. Call 'create_file' method first.")

        job = openai.FineTuningJob.create(training_file=file_id, model=self.model_name)
        self.job_id = job.id
        print(f"Job ID: {self.job_id}")

    def list_jobs(self, limit=10):
        jobs_data = openai.FineTuningJob.list(limit=limit)

        # Formatting the jobs_data for human-readable output
        formatted_output = format_jobs_output(jobs_data)

        print(formatted_output)
        return jobs_data

    def get_job_details(self, job_id=None):
        if job_id is None:
            job_id = self.job_id

        if job_id is None:
            raise ValueError("No training job started. Call 'start_training' method first.")

        stats = openai.FineTuningJob.retrieve(job_id)
        print(f"Stats: {stats}")
        return stats

    def cancel_job(self, job_id=None):
        if job_id is None:
            job_id = self.job_id

        if job_id is None:
            raise ValueError("No training job started. Call 'start_training' method first.")

        openai.FineTuningJob.cancel(job_id)

    def list_events(self, job_id=None, limit=10):
        if job_id is None:
            job_id = self.job_id

        if job_id is None:
            raise ValueError("No training job started. Call 'start_training' method first.")

        events = openai.FineTuningJob.list_events(id=job_id, limit=limit)
        print(f"Events: {events}")
        return events

    def delete_model(self, model_id=None):
        if model_id is None:
            model_id = self.model_id

        if model_id is None:
            raise ValueError("Model ID not provided. Set 'model_id' or pass as a parameter.")

        openai.Model.delete(model_id)


# Example Usage
# trainer = TrainGPT()
# trainer.create_file("path/to/file.jsonl")
# trainer.start_training()
# trainer.list_jobs()
# trainer.get_job_details()
# trainer.cancel_job()
# trainer.list_events()

def main():
    parser = argparse.ArgumentParser(description="Command Line Interface for TrainGPT")
    parser.add_argument("--create-file", type=str, help="Path to the file to be uploaded")
    parser.add_argument("--start-training", action="store_true",
                        help="Start a new training job using the uploaded file")
    parser.add_argument("--list-jobs", action="store_true", help="List all training jobs")
    parser.add_argument("--get-job-details", type=str, help="Get details for a specific job")
    parser.add_argument("--cancel-job", type=str, help="Cancel a specific job")
    parser.add_argument("--list-events", type=str, help="List events for a specific job")
    parser.add_argument("--delete-model", type=str, help="Delete a specific model")

    args = parser.parse_args()

    trainer = TrainGPT()

    if args.create_file:
        trainer.create_file(args.create_file)
    if args.start_training:
        trainer.start_training()
    if args.list_jobs:
        trainer.list_jobs()
    if args.get_job_details:
        trainer.get_job_details(args.get_job_details)
    if args.cancel_job:
        trainer.cancel_job(args.cancel_job)
    if args.list_events:
        trainer.list_events(args.list_events)
    if args.delete_model:
        trainer.delete_model(args.delete_model)


if __name__ == "__main__":
    main()
