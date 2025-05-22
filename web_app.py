from flask import Flask, render_template, request, jsonify
import os
import webbrowser
from main import analyze_pdf_pages, convert_pdf_to_images, split_pdf_by_chapters

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['file']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        action = request.form.get('action')
        if action == 'page_count':
            result = analyze_pdf_pages(filepath)
            return jsonify({
                'page_count': result[0],
                'size_stats': result[1]
            })
        elif action == 'convert_images':
            result = convert_pdf_to_images(filepath)
            if os.path.exists(result[0]):
                os.startfile(os.path.dirname(result[0]))
            return jsonify({'image_paths': result})
        elif action == 'split_chapters':
            result = split_pdf_by_chapters(filepath)
            if result and os.path.exists(result[0]['output_path']):
                os.startfile(os.path.dirname(result[0]['output_path']))
            return jsonify({'chapters': result})
    
    return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        webbrowser.open('http://localhost:5000')
    app.run(debug=True)