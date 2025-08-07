from flask import Flask, render_template, request , session

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # ⚠️ 實際使用請改為安全的密鑰

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # getlist 會抓到多個同名欄位 (checkbox, list 等)
        purpose_items = request.form.getlist('purpose_item')
        input_desc = request.form.get('input_desc')
        output_desc = request.form.get('output_desc')
        language = request.form.get('language')
        need_tests = request.form.get('need_tests')
        constraints = request.form.get('constraints')

        # 儲存到 session
        session['form_data'] = {
            'purpose_items': purpose_items,
            'input_desc': input_desc,
            'output_desc': output_desc,
            'language': language,
            'need_tests': need_tests,
            'constraints': constraints
        }

        # 組合條列式用途描述，加上數字標號
        purpose = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(purpose_items)])

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

    # GET request: 檢查是否有舊資料要還原
    form_data = session.get('form_data', None)
    return render_template('form.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
