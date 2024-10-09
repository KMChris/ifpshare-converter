from flask import Flask, render_template, request, send_file
from reportlab.pdfgen import canvas
import requests
import zipfile
import json
import io

app = Flask(__name__)

def create_pdf(url):
    uuid = url.split('/')[-2]
    response = requests.get('https://air.ifpshare.com/api/pub/files/' + uuid)
    response = json.loads(response.text)
    name = response['name']
    pdf_path = f'{name}.pdf'
    urls = [image['downloadUrl'] for image in response['items']]
    image_paths = []
    c = canvas.Canvas(f'{name}.pdf', pagesize=(1600, 900))
    for i, url in enumerate(urls):
        image = requests.get('https:' + url)
        image_path = f'{name}_{i}.png'
        image_paths.append(image_path)
        with open(image_path, 'wb') as file:
            file.write(image.content)
        c.drawImage(image_path, 0, 0, width=1600, height=900)
        c.showPage()
    c.setTitle(name)
    c.save()
    return pdf_path

def create_zip(url):
    uuid = url.split('/')[-2]
    response = requests.get('https://air.ifpshare.com/api/pub/files/' + uuid)
    response = json.loads(response.text)
    name = response['name']
    urls = [image['downloadUrl'] for image in response['items']]
    image_paths = []
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for i, url in enumerate(urls):
            image = requests.get('https:' + url)
            image_path = f'{name}_{i}.png'
            image_paths.append(image_path)
            zip_file.writestr(image_path, image.content)
    zip_buffer.seek(0)
    return zip_buffer, f'{name}.zip'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        url = request.form.get('url')
        action = request.form.get('action')
        if url:
            if not url.startswith("https://air.ifpshare.com/documentPreview.html"):
                return render_template('index.html', error="Invalid URL!")
            if action == 'download_pdf':
                pdf = create_pdf(url)
                response = send_file(pdf, as_attachment=True)
                response.headers['Content-Disposition'] = f'attachment; filename={pdf}'
                return response
            elif action == 'download_zip':
                zip_buffer, zip_filename = create_zip(url)
                response = send_file(zip_buffer, as_attachment=True, mimetype='application/zip', download_name=zip_filename)
                response.headers['Content-Disposition'] = f'attachment; filename={zip_filename}'
                return response
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
