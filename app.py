import asyncio
from flask import Flask, request, jsonify
from tera import terabox
from server import teraBoxDl
from tera2 import get_data

app = Flask(__name__)

async def get_terabox_data_async(url):
    try:
        download_link, file_name, file_size, thumb = await asyncio.to_thread(terabox, url)
        response_data = {
            'download_link': download_link,
            'file_name': file_name,
            'file_size': file_size,
            'thumb': thumb
        }
        return response_data
    except Exception as e:
        return {'error': str(e)}

@app.route('/api', methods=['GET'])
async def terabox_api():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is missing'}), 400

    response_data = await get_terabox_data_async(url)
    return jsonify(response_data)

@app.route('/api/dw', methods=['GET'])
async def get_download_link():
    data = request.args.get('data')
    if not data:
        return {"error": "Data parameter is missing"}, 400

    download_link = await teraBoxDl(data)
    return {"download_link": download_link}
    
@app.route('/api2', methods=['GET'])
async def get_download_data():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is missing"}), 400

    data = await get_data(url)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
      
