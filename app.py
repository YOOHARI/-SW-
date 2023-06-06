from flask import Flask, render_template, request
import openai
import io
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

openai.api_key = "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"

app = Flask(__name__)

def summarize(document):
    model_engine = "text-davinci-002"
    prompt = f"Summarize the given document in a few concise sentences:\n\n{document}\n\nSummary:"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=100
    )
    summary = response.choices[0].text
    return summary

def generate_answer(question, context):
    model_engine = "text-davinci-002"
    prompt = f"Provide a concise answer to the following question based on the given context:\n\nQuestion: {question}\nContext: {context}\nAnswer:"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=100
    )
    answer = response.choices[0].text
    return answer

def summarize_url(url):
    # Download the page and extract the text content
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.get_text()

    # Use OpenAI to summarize the text
    model_engine = "text-davinci-002"
    prompt = f"Summarize the content of the following URL in a few sentences:\n{url}"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=100
    )
    summary = response.choices[0].text
    return summary


def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def read_text_file(file):
    text = file.read().decode("utf-8")
    return text

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route("/url")
def url():
    return render_template("url.html")

@app.route("/input")
def input():
    return render_template("input.html")

@app.route("/summary", methods=["POST"])
def get_summary():
    document = request.form.get("document")
    file = request.files.get("file")
    if file:
        if file.filename.endswith(".pdf"):
            document = read_pdf(file)
        elif file.filename.endswith(".txt"):
            document = read_text_file(file)  # 텍스트 파일 읽기 추가
        elif file.filename.endswith(".hwp"):
            # Handle HWP file here (convert to text, extract content, etc.)
            pass
    summary = summarize(document)
    return render_template("result.html", summary=summary, document=document)

@app.route("/answer", methods=["POST"])
def get_answer():
    question = request.form.get("question")
    context = request.form.get("context")
    answer = generate_answer(question, context)
    return render_template("answer.html", answer=answer, question=question, context=context)

@app.route("/summary_url", methods=["POST"])
def get_summary_url():
    url = request.form.get("url")
    summary = summarize_url(url)
    return render_template("result_url.html", summary=summary, url=url)

if __name__ == "__main__":
    app.run(debug=True)
