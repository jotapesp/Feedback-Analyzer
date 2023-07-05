import pandas as pd
import gdown
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import openai
from json import dump, dumps, load, loads
import sys
import os

def validate_integer_range(text, max, min):
    while True:
        try:
            value = int(input(text))
            if not (min <= value <= max):
                raise ValueError(f"You must enter an integer value between {min} and {max}")
            return value
        except ValueError as e:
            print(f"Enter a valid option from the menu: {e}")

class Feedback:
    def __init__(self, score, comment):
        self.score = score
        self.comment = comment
        self.sentiment = ""
    def __str__(self):
        return f"{self.score:2} - {self.comment} - Sentiment: {self.sentiment}"

class FeedbackAnalyzer:
    def __init__(self, feedbacks):
        self.feedbacks = feedbacks

    def calculate_nps(self):
        promoters = sum([1 for feedback in self.feedbacks if feedback.score >= 9])
        detractors = sum([1 for feedback in self.feedbacks if feedback.score <= 6])
        return (promoters - detractors) / len(self.feedbacks) * 100

    def create_nps_chart(self, chart_img_name="nps_chart", delimit=";", language="pt-br"):
        if language == "pt-br":
            NPS_ZONAS = ['Crítico', 'Aperfeiçoamento', 'Qualidade', 'Excelência']
        elif language == "en-us":
            NPS_ZONAS = ['Critical/Needs improvement', 'Good', 'Great', 'Excelent']
        NPS_VALORES = [-100, 0, 50, 75, 100]
        NPS_CORES = ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4']

        fig, ax = plt.subplots(figsize=(10, 2))

        for i, zona in enumerate(NPS_ZONAS):
            ax.barh([0], width=NPS_VALORES[i+1] - NPS_VALORES[i], left=NPS_VALORES[i], color= NPS_CORES[i])

        ax.barh([0], width=1, left=self.calculate_nps(), color='black')
        ax.set_yticks([])
        ax.set_xlim(-100, 100)
        ax.set_xticks(NPS_VALORES)

        plt.text(self.calculate_nps(), 0, f"{self.calculate_nps():.2f}", ha='center', va='center', color='white', bbox=dict(facecolor='black'))

        patches = [mpatches.Patch(color=NPS_CORES[i], label=NPS_ZONAS[i]) for i in range(len(NPS_ZONAS))]
        plt.legend(handles=patches, bbox_to_anchor=(1,1))
        plt.savefig(f'{chart_img_name}.png', format='png', bbox_inches="tight")
        # plt.show()

    def generate_verbal_analysis(self, key, language="pt-br"):
        comments = "\n".join([f"- {feedback.comment}" for feedback in self.feedbacks])
        prompt = ""
        message = ""
        openai.api_key = key
        if language == "pt-br":
            prompt = f"""Analise os seguintes comentários, classificando-os como Positivo, Negativo ou Neutro e retornando apenas a classificação:
                        {comments}"""
            message = "Você é um modelo de análise de sentimentos com foco em feedback sobre experiências educacionais"
        if language == "en-us":
            prompt = f"""Analyze comments below, classifying them as Positive, Negative or Neutral, returning only their classifications:
                        {comments}"""
            message = "You are a sentiments analysis model focused on educational experiences feedbacks"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": message},
            {"role": "user", "content": prompt}
            ])
        sentiments = response.choices[0].message.content
        sentiments_list = sentiments.split("\n")
        for i in range(len(self.feedbacks)):
            self.feedbacks[i].sentiment = sentiments_list[i]
        prompt2 = ""
        if language == "pt-br":
            prompt2 = f"""Sintetize uma análise geral sobre os seguintes comentários:
                {comments}"""
        if language == "en-us":
            prompt2 = f"""Sinthetize a general analysis of the comments below:
                {comments}"""
        response2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "Você é um modelo de análise de sentimentos com foco em feedback sobre experiências educacionais"},
            {"role": "user", "content": prompt2}
            ])
        analysis = response2.choices[0].message.content
        with open("analysis.txt", "a") as file:
            for feedback in self.feedbacks:
                file.write(f"{feedback}\n")
            file.write(f"Analysis: {analysis}")


LANGUAGES = [
            ["Brazilian Portuguese", "pt-br"],
            ["English United States", "en-us"],
            ]

if __name__ == '__main__':
    if sys.argv[1] == 'settings' or sys.argv[1] == "configuracoes":
        print("Choose program language:")
        for ind, lan in enumerate(LANGUAGES):
            print(f"{ind}-{lan[0]}")
        language_op = validate_integer_range("Choose an option: ", len(LANGUAGES),
                                            0)
        language = LANGUAGES[language_op][1]
        delim = input("Choose CSV file delimiter or leave blank for default ';':")
        if not delim.strip():
            delim = "0"
        openai_api_key = input("Enter OpenAI API key to be used or blank for default trial: ")
        if not openai_api_key.strip():
            openai_api_key = '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'
        settings = {"language": language,
                    "delim": delim,
                    "openai_api_key": openai_api_key,}
        with open("settings.json", "w") as file:
            dump(settings, file)
    else:
        if not os.path.exists("settings.json"):
            print("First time using the app, you should use command")
            print("     `python fbapp.py settings`")
            print("to set initial settings.")
        else:
            if len(sys.argv) > 2:
                print("Usage: python fbapp.py [file_name]")
            else:
                filename = ""
                if "http" in sys.argv[1]:
                    gdown.download(sys.argv[1], "feedbacks.csv")
                    filename = "feedbacks.csv"
                else:
                    filename = sys.argv[1]
                settings = ""
                with open("settings.json", "r") as file:
                    settings = load(file)
                language = settings["language"]
                openai_api_key = settings["openai_api_key"]
                delim = settings["delim"]

                if delim == "0":
                    delim = ";"
                try:
                    dados = pd.read_csv(filename, delimiter=delim)
                    feedbacks = [Feedback(line["nota"], line["comentario"]) for ind, line in dados.iterrows()]
                    analyzer = FeedbackAnalyzer(feedbacks)
                    analyzer.create_nps_chart(chart_img_name="nps_chart", delimit=delim, language=language)
                    analyzer.generate_verbal_analysis(openai_api_key, language=language)
                except Exception as e:
                    print(f"An error ocurred: {e}")
                else:
                    print("Files generated in the root directory.")
