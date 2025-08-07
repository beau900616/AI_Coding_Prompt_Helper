from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        purpose = request.form.get('purpose')
        input_desc = request.form.get('input_desc')
        output_desc = request.form.get('output_desc')
        language = request.form.get('language')
        need_tests = request.form.get('need_tests')
        constraints = request.form.get('constraints')

        prompt = f"""請幫我用 {language} 寫一段程式，功能如下：

用途：
{purpose}

輸入說明：
{input_desc}

輸出說明：
{output_desc}

限制與其他需求：
{constraints if constraints else '無'}

是否需要單元測試：
{need_tests}

請給我完整的程式碼。"""

        return render_template('result.html', prompt=prompt)

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
