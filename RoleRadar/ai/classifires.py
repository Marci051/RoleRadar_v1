import re
import string
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score, balanced_accuracy_score
)

import os
import joblib

from django.conf import settings
from collections import Counter


class Classifier:
    def __init__(self, model, tfidf=None):
        if type(model) == str:
            self.model = joblib.load(model)
        else:
            self.model = model

        if tfidf is not None:
            if type(tfidf) == str:
                self.tfidf = joblib.load(tfidf)
            else:
                self.tfidf = tfidf
        else:
            self.tfidf = None

    def train(self, x_train, y_train):
        self.model.fit(x_train, y_train)

    def evaluate(self, x_test, y_test):
        y_pred = self.model.predict(x_test)

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(20, 20))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=self.model.classes_, yticklabels=self.model.classes_)
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
        plt.show()

        # Accuracy
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.4f}")

        # Balanced Accuracy (for imbalanced datasets)
        balanced_acc = balanced_accuracy_score(y_test, y_pred)
        print(f"Balanced Accuracy: {balanced_acc:.4f}")

        # Precision (macro, micro, weighted)
        precision_macro = precision_score(y_test, y_pred, average='macro')
        precision_micro = precision_score(y_test, y_pred, average='micro')
        precision_weighted = precision_score(y_test, y_pred, average='weighted')
        print(f"Precision (Macro): {precision_macro:.4f}")
        print(f"Precision (Micro): {precision_micro:.4f}")
        print(f"Precision (Weighted): {precision_weighted:.4f}")

        # Recall
        recall_macro = recall_score(y_test, y_pred, average='macro')
        recall_micro = recall_score(y_test, y_pred, average='micro')
        recall_weighted = recall_score(y_test, y_pred, average='weighted')
        print(f"Recall (Macro): {recall_macro:.4f}")
        print(f"Recall (Micro): {recall_micro:.4f}")
        print(f"Recall (Weighted): {recall_weighted:.4f}")

        # F1 Score
        f1_macro = f1_score(y_test, y_pred, average='macro')
        f1_micro = f1_score(y_test, y_pred, average='micro')
        f1_weighted = f1_score(y_test, y_pred, average='weighted')
        print(f"F1 Score (Macro): {f1_macro:.4f}")
        print(f"F1 Score (Micro): {f1_micro:.4f}")
        print(f"F1 Score (Weighted): {f1_weighted:.4f}")

    def save(self, save_path):
        directory = os.path.dirname(save_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

        joblib.dump(self.model, save_path)

    @staticmethod
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = text.strip()
        return text

    def test(self, x):
        cleaned_resume = self.clean_text(x)
        if self.tfidf is None:
            raise ValueError("Invalid TF/IDF")
        else:
            x = self.tfidf.transform([cleaned_resume])

        predicted_job = self.model.predict(x)[0]
        return predicted_job


class TestClassifier:
    classes = ['Accountant', 'Agriculture', 'Apparel', 'Artist', 'Arts', 'Author',
               'Automation Testing', 'Automobile', 'Aviation', 'BPO', 'Backend Developer',
               'Banking', 'Blockchain', 'Business Analyst', 'Business Development', 'Chef',
               'Cloud Architect', 'Cloud Engineer', 'Construction Engineer', 'Consultant',
               'Customer Service Representative', 'Cybersecurity Analyst',
               'Data Scientist', 'Database Developer and Analyst', 'Designer',
               'DevOps Engineer', 'Developer', 'Digital Media', 'DotNet Developer',
               'ETL Developer', 'Electrical Engineer', 'Engineering',
               'Environmental Scientist', 'Event Planner', 'Finance', 'Fitness Coach',
               'Frontend Developer', 'Full Stack Developer', 'HR', 'Hadoop', 'Healthcare',
               'Information Technology', 'Java Developer', 'Lawyer',
               'Machine Learning Engineer', 'Mechanical Engineer', 'Mobile App Developer',
               'Network Engineer', 'Nurse', 'Operations Manager', 'Project Manager',
               'Public Relations', 'Python Developer', 'QA', 'Researcher', 'SAP Developer',
               'SEO Specialist', 'Sales', 'Social Worker', 'Teacher', 'Testing',
               'Web Designer', 'Web Developer']

    def __init__(self):
        self.models = []
        for key, value in settings.CLASSIFIERS.items():
            model = Classifier(value, tfidf=settings.TFIDF)
            self.models.append({
                key: model,
            })

    def predict(self, x):
        results = []
        for model_dict in self.models:
            for model_name, model in model_dict.items():
                output = model.test(x)
                if model_name == 'MLP':
                    output = self.classes[output]
                results.append({model_name: output})

        all_values = []

        for item in results:
            all_values.extend(item.values())
        value_counts = Counter(all_values)
        top_3_values = [value for value, count in value_counts.most_common(3)]
        return results, top_3_values
