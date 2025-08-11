from flask import Flask, render_template, request , session

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # ⚠️ 實際使用請改為安全的密鑰

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # getlist 會抓到多個同名欄位 (checkbox, list 等)
        purpose_items = request.form.getlist('purpose_item')
        terms_and_definitions = request.form.get('terms_and_definitions')
        references = request.form.get('references')
        language = request.form.get('language')
        design_method = request.form.get('design_method')
        system_structure = request.form.get('system_structure')
        input_data_explain = request.form.get('input_data_explain')
        output_data_explain = request.form.get('output_data_explain')
        constraints = request.form.get('constraints')

        # 儲存到 session
        session['form_data'] = {
            'purpose_items': purpose_items,
            'terms_and_definitions': terms_and_definitions,
            'references': references,
            'language': language,
            'design_method': design_method,
            'system_structure': system_structure,
            'input_data_explain':input_data_explain,
            'output_data_explain':output_data_explain,
            'constraints':constraints
        }

        # 組合條列式用途描述，加上數字標號
        purpose_list = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(purpose_items)])

        # 用三引號多行字串組合
        prompt = (
        "你是一位資深全端工程師，請根據以下技術文件撰寫完整且可執行的程式碼，"
        "包含必要的註解、程式結構以及最佳實踐。"
        "\n\n=== 文件開始 ==="
        "\n[前言 - 文件目的]\n"
        f"{purpose_list or '無'}"
        "\n\n[名詞解釋]\n"
        f"{terms_and_definitions or '無'}"
        "\n\n[參考資料]\n"
        f"{references or '無'}"
        "\n\n[軟體設計規劃]"
        "\n使用語言：\n"
        f"{language}"
        "\n設計方法與工具：\n"
        f"{design_method or '無'}"
        "\n系統架構：\n"
        f"{system_structure or '無'}"
        "\n\n[輸入資料型態說明]\n"
        f"{input_data_explain or '無'}"
        "\n\n[輸出資料型態說明]\n"
        f"{output_data_explain or '無'}"
        "\n\n[限制與其他需求]\n"
        f"{constraints or '無'}"
        "\n=== 文件結束 ==="
        "\n\n請依照上述技術文件，輸出完整的程式碼，並確保："
        "\n1. 程式碼可以直接執行"
        "\n2. 加入必要註解"
        "\n3. 保持程式可維護性")

        return render_template('result.html', prompt=prompt)

    # GET request: 檢查是否有舊資料要還原
    form_data = session.get('form_data', None)
    return render_template('form.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)
