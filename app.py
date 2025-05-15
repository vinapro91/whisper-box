from flask import Flask, request, jsonify
import tempfile
import os
import whisper
from werkzeug.utils import secure_filename
import threading
import uuid
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

model = whisper.load_model("base")

transcription_tasks = {}
transcription_metadata = {}

def transcribe_in_background(task_id, file_path):
    logging.info(f'Iniciando transcrição para task_id={task_id}, arquivo={file_path}')
    try:
        result = model.transcribe(file_path)
        transcription = result.get('text', '').strip()
        transcription_tasks[task_id] = {'status': 'done', 'transcription': transcription}
        logging.info(f'Resultado completo da transcrição para task_id={task_id}: {result}')
        logging.info(f'Transcrição concluída para task_id={task_id}')
    except Exception as e:
        transcription_tasks[task_id] = {'status': 'error', 'error': str(e)}
        logging.error(f'Erro na transcrição para task_id={task_id}: {e}')
    finally:
        try:
            os.remove(file_path)
            logging.info(f'Arquivo temporário removido: {file_path}')
        except Exception as e:
            logging.warning(f'Erro ao remover arquivo temporário {file_path}: {e}')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    logging.info('Recebendo requisição de transcrição')
    if 'file' not in request.files:
        logging.warning('Nenhum arquivo enviado na requisição')
        return jsonify({'error': 'No file sent.'}), 400
    file = request.files['file']
    if file.filename == '':
        logging.warning('Nome de arquivo vazio recebido')
        return jsonify({'error': 'Empty filename.'}), 400
    try:
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp:
            file.save(temp.name)
            temp.flush()
            task_id = str(uuid.uuid4())
            transcription_tasks[task_id] = {'status': 'processing'}
            logging.info(f'Arquivo salvo temporariamente em {temp.name}, task_id={task_id}')
            thread = threading.Thread(target=transcribe_in_background, args=(task_id, temp.name))
            thread.start()
        return jsonify({'task_id': task_id}), 202
    except Exception as e:
        logging.error(f'Erro ao processar o arquivo: {e}')
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/transcription_status/<task_id>', methods=['GET'])
def get_transcription_status(task_id):
    task = transcription_tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task ID not found.'}), 404
    if task['status'] == 'processing':
        return jsonify({'status': 'processing'}), 202
    elif task['status'] == 'done':
        return jsonify({'status': 'done', 'transcription': task['transcription']}), 200
    else:
        return jsonify({'status': 'error', 'error': task.get('error', 'Unknown error')}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
