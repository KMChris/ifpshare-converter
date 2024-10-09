from flask import Flask, render_template, request, send_file, jsonify
from reportlab.pdfgen import canvas
import requests
import zipfile
import json
import io

app = Flask(__name__)

def create_pdf(url):
    uuid = url.split('/')[-2]
    try:
        response = requests.get('https://air.ifpshare.com/api/pub/files/' + uuid)
        response.raise_for_status()
        data = json.loads(response.text)
        name = data['name']
        pdf_path = f'{name}.pdf'
        urls = [image['downloadUrl'] for image in data['items']]
    except requests.RequestException as e:
        if response.status_code == 404:
            return None, 'Document expired or does not exist'
        elif response.status_code in (412, 500):
            return None, 'URL is not a valid IFPShare document URL'
        return None, f'Error: {e}'
    if not urls:
        return None, 'No images found in document'
    image_paths = []
    c = canvas.Canvas(f'{name}.pdf', pagesize=(1600, 900))
    for i, url in enumerate(urls):
        try:
            image = requests.get('https:' + url)
            image.raise_for_status()
        except requests.RequestException as e:
            return None, f'Could not download image: {e}'
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
    try:
        response = requests.get('https://air.ifpshare.com/api/pub/files/' + uuid)
        response.raise_for_status()
        data = json.loads(response.text)
        name = data['name']
        urls = [image['downloadUrl'] for image in data['items']]
    except requests.RequestException as e:
        if response.status_code == 404:
            return None, 'Document expired or does not exist'
        elif response.status_code in (412, 500):
            return None, 'URL is not a valid IFPShare document URL'
        return None, f'Error: {e}'
    if not urls:
        return None, 'No images found in document'
    image_paths = []
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for i, url in enumerate(urls):
            try:
                image = requests.get('https:' + url)
                image.raise_for_status()
            except requests.RequestException as e:
                return None, f'Could not download image: {e}'
            image_path = f'{name}_{i}.png'
            image_paths.append(image_path)
            zip_file.writestr(image_path, image.content)
    zip_buffer.seek(0)
    return zip_buffer, f'{name}.zip'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        action = request.form.get('action')
        if url:
            if not url.startswith("https://air.ifpshare.com/documentPreview.html"):
                return jsonify(error="URL must be a valid IFPShare document URL"), 400
            if action == 'download_pdf':
                result = create_pdf(url)
                if isinstance(result, tuple) and result[0] is None:
                    return jsonify(error=result[1]), 500
                pdf = result
                response = send_file(pdf, as_attachment=True)
                response.headers['Content-Disposition'] = f'attachment; filename={pdf}'
                return response
            elif action == 'download_zip':
                result = create_zip(url)
                if result[0] is None:
                    return jsonify(error=result[1]), 500
                zip_buffer, zip_filename = result
                response = send_file(zip_buffer, as_attachment=True, mimetype='application/zip', download_name=zip_filename)
                response.headers['Content-Disposition'] = f'attachment; filename={zip_filename}'
                return response
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)
