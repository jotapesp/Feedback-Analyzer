# Feedback Comments Analyzer

(EN-US) This is a Feedback analyzer application created with ChatGPT with the purpose to analyze the sentiments expressed in feedback comments sent by users and generate a general analysis based on all those comments received. In addition, the app also generates a NET Promoter score (NPS) chart according to the feedback scores.

(PT-BR) Essa é uma aplicação criada com ChatGPT com o propósito de analisar os sentimentos expressos por comentários de feedbacks enviados por usuários, gerando uma análise geral de todos esses comentários. Além disso, o programa também gera um gráfico com o NET Promoter score (NPS) de acordo com as notas nos feedbacks.

### Built With

[![Python](https://img.shields.io/badge/Python-000?style=for-the-badge&logo=python)](https://docs.python.org/3/)
[![OpenAI](https://img.shields.io/badge/openai-000?style=for-the-badge&logo=openai)](https://sqlite.com/docs.html)

### Usage

(EN-US)
If it is the first time running the program, it should be run on the terminal using the command
`python fbapp.py settings` to set preferences and OpenAI API Key (you can leave it blank to use the default one, but it is a trial key and may be deprecated).
After that, it can be run using command `python fbapp.py csv-filename/link-to-download-file`. <br>
ATTENTION!<br>
* In case the filename is passed as an argument in the commandline, the file should be located in the same folder as `fbapp.py`.
* In case you prefer to pass a link to download the file, it should be the full link, example: `https://https://drive.google.com/uc?id={file_id}`
The file containing the feedbacks scores and comments to be analyzed should be a CSV file. The default delimiter parameter used in this application is semicolon (;) but it can be changed to anyother character using command `python fbapp.py settings`

(PT-BR)
Para rodar o programa, abra o terminal e use o comando
`python fbapp.py configuracoes` para ajustar as preferências e a chave do OpenAI API (caso não tenha uma chave, pode deixar em branco para usar a default, mas ela é uma chave de teste e pode estar expirada). Depois disso, o programa pode ser rodado usando o comando `python fbapp.py nome-do-arquivo-csv/link-para-baixar-o-arquivo`.
ATENÇÃO!<br>
* Caso escolha passar o nome do arquivo na linha de comando, o arquivo deve estar localizado na mesma pasta que o arquivo `fbapp.py`.
* Caso prefira passar o link do arquivo a ser baixado e analisado, o link deve estar completo, por exemplo: `https://https://drive.google.com/uc?id={file_id}`
O arquivo contendo os comentários e as notas dos feedbacks devem ser um arquivo CSV. O delimiter padrão utilizado é o ponto e vírgula (;) mas pode ser alterado para qualquer caractere utilizando o comando `python fbapp.py configuracoes`

CSV File example:
![Imgur](https://i.imgur.com/fclzApl.png)
![Imgur](https://i.imgur.com/BLZkNT6.png)


### Outputs
(EN-US)
The program will generate a PNG file (`nps_chart.png`)  containing the NPS chart and a txt file (`analysis.txt`) with the feedbacks analysis in the same directory as the file `fbapp.py` <br>

(PT-BR)
O programa gerará um arquivo PNG (`nps_chart.png`) contendo o gráfico NPS e um arquivo txt (`analysis.txt`) com a análise dos feedbacks no mesmo diretório que o arquivo `fbapp.py` <br>

* NPS Chart example:
![Imgur](https://i.imgur.com/OB06VAL.png)
<br>

* Analysis file example:
![Imgur](https://i.imgur.com/plxqMN8.png)

### Requirements

The dependencies are listed in the requirements.txt file linked below.

* [requirements.txt](https://github.com/jotapesp/)
