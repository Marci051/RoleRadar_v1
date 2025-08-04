import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('dark_background')

# Load Data
df = pd.read_csv('datasets/Job-Description-Dataset.csv')


# Preprocessing Data
def extract_avg_experience(exp_str):
    match = re.match(r'(\d+)\s*to\s*(\d+)', exp_str)
    if match:
        low = int(match.group(1))
        high = int(match.group(2))
        return (low + high) / 2
    else:
        return None


def parse_salary(s):
    s = s.replace('$', '').replace('K', '')
    low, high = s.split('-')
    return (float(low) + float(high)) / 2


df['Experience'] = df['Experience'].apply(extract_avg_experience)
df['Salary Range'] = df['Salary Range'].apply(parse_salary)

###########################################################################
# Experience (Top 20 Job Titles by Average Experience)
mean_experience = df.groupby('Job Title')['Experience'].mean()
mean_experience_sorted = mean_experience.sort_values(ascending=False)

top_20 = mean_experience_sorted.head(20).reset_index()
top_20.columns = ['Job Title', 'Average Experience']

plt.figure(figsize=(12, 8))
plt.barh(top_20['Job Title'], top_20['Average Experience'], color=plt.cm.viridis(np.linspace(0, 1, len(top_20))))
plt.gca().invert_yaxis()
plt.title('Top 20 Job Titles by Average Experience Required', fontsize=16)
plt.xlabel('Average Years of Experience', fontsize=12)
plt.ylabel('Job Title', fontsize=12)
plt.tight_layout()
plt.show()

###########################################################################
# Qualifications (Top 10 by Count)
qualification_counts = df['Qualifications'].value_counts().head(10)
qual_df = qualification_counts.reset_index()
qual_df.columns = ['Qualification', 'Count']

plt.figure(figsize=(10, 6))
plt.barh(qual_df['Qualification'], qual_df['Count'], color=plt.cm.plasma(np.linspace(0, 1, len(qual_df))))
plt.gca().invert_yaxis()
plt.title('Top 10 Qualifications by Count', fontsize=16)
plt.xlabel('Number of Records', fontsize=12)
plt.ylabel('Qualification', fontsize=12)
plt.tight_layout()
plt.show()

###########################################################################
# Salary Range (Top 20 Job Titles by Average Salary)
salary_by_title = df.groupby('Job Title')['Salary Range'].mean().sort_values(ascending=False).head(20)
salary_df = salary_by_title.reset_index()

plt.figure(figsize=(12, 8))
plt.barh(salary_df['Job Title'], salary_df['Salary Range'], color=plt.cm.coolwarm(np.linspace(0, 1, len(salary_df))))
plt.gca().invert_yaxis()
plt.title('Top 20 Job Titles by Average Salary', fontsize=16)
plt.xlabel('Average Salary (in K)', fontsize=12)
plt.ylabel('Job Title', fontsize=12)
plt.tight_layout()
plt.show()

###########################################################################
# Country (Top 20 Countries by Number of Jobs)
country_counts = df['Country'].value_counts().head(20)
country_df = country_counts.reset_index()
country_df.columns = ['Country', 'Count']

plt.figure(figsize=(12, 8))
plt.barh(country_df['Country'], country_df['Count'], color=plt.cm.twilight(np.linspace(0, 1, len(country_df))))
plt.gca().invert_yaxis()
plt.title('Top 20 Countries by Number of Jobs', fontsize=16)
plt.xlabel('Number of Jobs', fontsize=12)
plt.ylabel('Country', fontsize=12)
plt.tight_layout()
plt.show()

###########################################################################
# Work Type (Top 20 by Count)
work_type_counts = df['Work Type'].value_counts().head(20)
work_df = work_type_counts.reset_index()
work_df.columns = ['Work Type', 'Count']

plt.figure(figsize=(12, 8))
plt.barh(work_df['Work Type'], work_df['Count'], color=plt.cm.seismic(np.linspace(0, 1, len(work_df))))
plt.gca().invert_yaxis()
plt.title('Top Work Types by Number of Records', fontsize=16)
plt.xlabel('Number of Records', fontsize=12)
plt.ylabel('Work Type', fontsize=12)
plt.tight_layout()
plt.show()
