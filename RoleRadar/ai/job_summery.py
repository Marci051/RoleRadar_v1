import pandas as pd
from rapidfuzz import fuzz
from django.conf import settings

from ai.gemini import fetch_gemini_response


class JobSummery:
    def __init__(self):
        self.job_dataset = pd.read_csv('ai/datasets/Job-Description-Dataset.csv')

    def find_similar_title(self, field_name):
        unique_jobs = self.job_dataset['Job Title'].unique()

        results = []
        for job in unique_jobs:
            score = fuzz.token_sort_ratio(field_name, job)
            if score >= settings.THRESHOLD_SCORE:
                results.append((job, score))

        results = sorted(results, key=lambda x: x[1], reverse=True)

        return results

    def get_job_summery(self, field_name):
        results = self.find_similar_title(field_name)
        if len(results) == 0:
            print(f"No local match found for '{field_name}'. Querying Gemini for a general summary.")
            try:
                prompt = f"Describe the key responsibilities and provide a **concise** general summary for a {field_name} role. Please ensure the response is **no more than 6 lines**."
                summary = fetch_gemini_response(prompt_content=prompt)
                return summary
            except Exception as e:
                print(f"Error fetching summary from Gemini for '{field_name}': {type(e).__name__} - {e}")
                return "Sorry, an error occurred while trying to get the job summary from the assistant."

            # return "Job not found :("

        else:
            job_titles_only = [job for job, score in results]
            filtered_dataset = self.job_dataset[self.job_dataset['Job Title'].isin(job_titles_only)]
            descriptions = filtered_dataset['Job Description'].tolist()
            combined_descriptions = "\n".join(descriptions)
            text = f"Summarize the following tasks so that important topics are not lost. \n {combined_descriptions}"
            output = fetch_gemini_response(prompt_content=text)
            return results, output
