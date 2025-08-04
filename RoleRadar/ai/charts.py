import re
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

plt.style.use('dark_background')

df = pd.read_csv('ai/datasets/Job-Description-Dataset.csv')


def extract_avg_experience(exp_str):
    match = re.match(r'(\d+)\s*to\s*(\d+)', str(exp_str))
    if match:
        low = int(match.group(1))
        high = int(match.group(2))
        return (low + high) / 2
    else:
        return None


def parse_salary(s):
    s = str(s).replace('$', '').replace('K', '')
    if '-' in s:
        low, high = s.split('-')
        return (float(low) + float(high)) / 2
    else:
        return None


df['Experience'] = df['Experience'].apply(extract_avg_experience)
df['Salary Range'] = df['Salary Range'].apply(parse_salary)


# Helper to convert matplotlib figure to base64 string
def fig_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + string.decode('utf-8')
    buf.close()
    plt.close()
    return uri


def custom_analyze(job_title):
    filtered_df = df[df['Job Title'].str.strip().str.lower() == job_title.lower()]

    results = {}

    # Experience
    mean_experience = filtered_df['Experience'].mean()
    results['mean_experience'] = f"{mean_experience:.2f} years" if pd.notnull(mean_experience) else "N/A"

    # Qualifications pie
    qualification_counts = filtered_df['Qualifications'].value_counts()
    qualification_percent = (qualification_counts / qualification_counts.sum()) * 100
    plt.figure(figsize=(6, 6))
    plt.pie(
        qualification_percent,
        labels=qualification_percent.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors
    )
    plt.title(f'Qualification Distribution for {job_title} Jobs')
    results['qualification_chart'] = fig_to_base64()

    # Salary
    mean_salary = filtered_df['Salary Range'].mean()
    results['mean_salary'] = f"${mean_salary:.2f}K" if pd.notnull(mean_salary) else "N/A"

    # Country bar
    country_counts = filtered_df['Country'].value_counts().head(20)
    country_df = country_counts.reset_index()
    country_df.columns = ['Country', 'Count']
    plt.figure(figsize=(8, 6))
    sns.barplot(data=country_df, x='Count', y='Country', hue='Country', dodge=False, palette='coolwarm')
    plt.title(f'Top 20 Countries Posting {job_title} Jobs')
    plt.xlabel('Number of Job Posts')
    plt.ylabel('Country')
    plt.legend([], [], frameon=False)
    results['country_chart'] = fig_to_base64()

    # Work Type pie
    worktype_counts = filtered_df['Work Type'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(
        worktype_counts,
        labels=worktype_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Paired.colors
    )
    plt.title(f'Work Type Distribution for {job_title} Jobs')
    results['worktype_chart'] = fig_to_base64()

    # Preference pie
    preference_counts = filtered_df['Preference'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(
        preference_counts,
        labels=preference_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.Set3.colors
    )
    plt.title(f'Preference Distribution for {job_title} Jobs')
    results['preference_chart'] = fig_to_base64()

    # Company Size
    average_size = filtered_df['Company Size'].mean()
    results['average_company_size'] = f"{round(average_size)}" if pd.notnull(average_size) else "N/A"

    # Role pie
    role_counts = filtered_df['Role'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(
        role_counts,
        labels=role_counts.index,
        autopct='%1.1f%%',
        startangle=140,
        colors=plt.cm.tab20.colors
    )
    plt.title(f'Role Distribution for {job_title} Jobs')
    results['role_chart'] = fig_to_base64()

    return results
