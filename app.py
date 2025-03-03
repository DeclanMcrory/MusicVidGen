from flask import Flask, request, render_template, redirect, url_for
import os
from generator import MusicVideoGenerator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['GENERATED_FOLDER'] = 'static/generated/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)

# Initialize the generator
generator = MusicVideoGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        # Save the uploaded audio file
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(audio_path)
        
        # Generate the video
        output_filename = file.filename.rsplit('.', 1)[0] + '.mp4'
        output_path = os.path.join(app.config['GENERATED_FOLDER'], output_filename)
        
        try:
            generator.generate(audio_path, output_path)
            return redirect(url_for('result', filename=file.filename))
        except Exception as e:
            return render_template('error.html', error=str(e))

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)