## 문서 요약 프로그램
### 구체적인 기능
사용자가 요약하고자 하는 내용을 총 3가지 기능을 이용해 제공받을 수 있음
1. 직접 입력 : 사용자가 요약하고자 하는 내용을 텍스트 창에 직접 입력하여 요약 결과를 받을 수 있음
2. 파일 업로드 : 사용자가 pdf 또는 txt 형식의 파일을 업로드하여 요약 결과를 받을 수 있음
3. URL 주소 입력 : 요약하고자 하는 URL의 주소를 입력하여 요약 결과를 받을 수 있음
### 개발 언어
*  Back-end : Python
*  Front-end : Html CSS Javascript
### 상세 설계
1. Back-end
*  summarize(document) : document를 입력으로 받아 OpenAI의 text-davinci-002 모델을 사용하여 문서의 간결한 요약을 생성
```python
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
```
*  summrize_url(url) : url을 입력으로 받아 requests.get() 메서드를 사용하여 웹 페이지를 다운로드하고 BeautifulSoup라이브러리를 사용하여 텍스트 내용을 추출한 뒤 OpenAI의 text-davince-002 모델을 사용하여 텍스트이 간결한 요약을 생성
```python
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
```    
*  generate_answer(question, context) : question과 context를 입력으로 받아 OpenAI의 text-davinci-002모델을 사용하여 주어진 문맥에 기반한 답변 생성
```python
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
```      
*  read_pdf(file) : file객체를 입력으로 받아 pyPDF2라이브러리를 사용하여 PDF에서 텍스트내용을 읽어와 메    서드를 사용하여 텍스트 추출
```python
def read_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text
```    
*  read_text_file(file) : file객체(txt파일)을 입력으로 받아 메세드를사용하여 UTF-8 인코딩 된 텍스트로 내용을     읽어와 디코딩된 텍스트를 반환
```python
def read_text_file(file):
    text = file.read().decode("utf-8")
    return text
```
*  get_summary() : 문서를요약하는 POST 요청을 처리, 입력된 문서(직접입력 or파일 업로드)를 가져오고 문서    의 종류(pdf or txt)를 결정된 후 적절한 함수를 호출하여 요약을 생성
```python
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
```
*  get_answer() : 주어진 문맥을 기반으로 질문에 대한 답변을 생성하는 POST 요청을 처리
```python
def get_answer():
    question = request.form.get("question")
    context = request.form.get("context")
    answer = generate_answer(question, context)
    return render_template("answer.html", answer=answer, question=question, context=context)
```
*  get_summary_url() : url을 입력하여 웹 페이지를 요약하는 POST 요청을 처리
```python
def get_summary_url():
    url = request.form.get("url")
    summary = summarize_url(url)
    return render_template("result_url.html", summary=summary, url=url)
```
### 프로그램 사용법

