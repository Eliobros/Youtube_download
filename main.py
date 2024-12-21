import os
import time
from flask import Flask, jsonify, request
import yt_dlp

app = Flask(__name__)

# Função para extrair informações do vídeo
def get_video_info(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extractaudio': True,  # Extrair áudio
        'noplaylist': True,
        'forcejson': True,  # Força saída em JSON
    }

    # Inicializa o yt-dlp com as opções
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info:
            video_info = info['entries'][0]  # Pega o primeiro resultado da busca

            title = video_info['title']
            thumbnail_url = video_info['thumbnail']
            video_id = video_info['id']
            channel = video_info['uploader']
            video_url = video_info['webpage_url']
            views = video_info['view_count']
            publish_date = video_info['upload_date']
            description = video_info.get('description', 'Sem descrição')

            # Gera links de download temporários (5 minutos)
            temp_audio_url = f"http://example.com/download/audio/{video_id}"  # Substitua com o link real
            temp_video_url = f"http://example.com/download/video/{video_id}"  # Substitua com o link real

            # Definindo o tempo de expiração
            expire_time = time.time() + 300  # 5 minutos (em segundos)

            return {
                'title': title,
                'thumbnail_url': thumbnail_url,
                'video_id': video_id,
                'channel': channel,
                'video_url': video_url,
                'views': views,
                'publish_date': publish_date,
                'description': description,
                'audio_download_link': temp_audio_url,
                'video_download_link': temp_video_url,
                'expire_time': expire_time
            }
    return None

# Rota para fornecer a documentação da API
@app.route('/api/youtube', methods=['GET'])
def api_documentation():
    documentation = {{
  "autor": "Habibo Salimo",
  "empresa": "Eliobros Tech",
  "version": "1.0.0",
  "lançamento": "20 de dezembro de 2024",
  "description": "Esta API permite buscar vídeos no YouTube com base em uma consulta e fornecer links de download temporários para áudio e vídeo.",
  "endpoints": {
    "/api/youtube": {
      "method": "GET",
      "description": "Retorna a documentação da API, onde você encontra todos os detalhes sobre como usar a API.",
      "parameters": {}
    },
    "/api/youtube/download": {
      "method": "GET",
      "description": "Retorna informações sobre o vídeo e links de download com base na consulta.",
      "parameters": {
        "query": {
          "type": "string",
          "description": "Nome da música ou vídeo a ser pesquisado no YouTube."
        }
      }
    }
  },
  "forma de uso": {
    "example_request": "/api/youtube/download?query=nome_da_musica",
    "response": {
      "title": "Título do vídeo",
      "thumbnail_url": "URL da thumbnail",
      "video_id": "ID do vídeo",
      "channel": "Nome do canal",
      "video_url": "URL do vídeo no YouTube",
      "views": "Número de visualizações",
      "publish_date": "Data de publicação",
      "description": "Descrição do vídeo",
      "audio_download_link": "Link para download do áudio",
      "video_download_link": "Link para download do vídeo",
      "expire_time": "Timestamp de expiração dos links"
    }
  },
  "exemplo_de_codigo": {
    "Python": "import requests\n\nurl = 'http://example.com/api/youtube/download'\nparams = {'query': 'Despacito Luis Fonsi'}\nresponse = requests.get(url, params=params)\nif response.status_code == 200:\n  data = response.json()\n  print(f'Título: {data['title']}')\n  print(f'Link de áudio: {data['audio_download_link']}')\n  print(f'Link de vídeo: {data['video_download_link']}')",
    "JavaScript": "fetch('http://example.com/api/youtube/download?query=Despacito Luis Fonsi')\n  .then(response => response.json())\n  .then(data => {\n    console.log('Título:', data.title);\n    console.log('Link de áudio:', data.audio_download_link);\n    console.log('Link de vídeo:', data.video_download_link);\n  });"
  },
  "FAQ": {
    "expiração_do_link_de_download": "Os links fornecidos têm duração de 5 minutos. Após esse tempo, os links serão invalidados.",
    "posso_clicar_no_link_mais_de_uma_vez": "Não. Uma vez que o link é gerado, ele será invalidado após o primeiro clique. Isso é feito para garantir a segurança.",
    "os_dois_links_têm_a_mesma_duração": "Sim, tanto os links de áudio quanto os de vídeo expiram após 5 minutos."
  },
  "limitações_e_restrições": {
    "limites_de_uso": "A API permite até 100 requisições por minuto por IP.",
    "restricoes_de_uso": "A API não deve ser usada para baixar conteúdos protegidos por direitos autorais."
  },
  "código_status_http": {
    "200": "OK - Requisição bem-sucedida.",
    "400": "Bad Request - Parâmetro 'query' ausente.",
    "404": "Not Found - Nenhum vídeo encontrado.",
    "500": "Internal Server Error - Erro no servidor."
  },
  "termos_de_uso": {
    "descricao": "O uso da API está sujeito aos seguintes termos. Ao utilizar a API, você concorda com as condições aqui descritas. A Eliobros Tech se reserva o direito de modificar os termos de uso a qualquer momento.",
    "política_de_privacidade": "As informações coletadas são usadas exclusivamente para fornecer os serviços da API e não serão compartilhadas com terceiros sem o consentimento do usuário."
  }
  "Suporte e Redes sociais ": {
    "Whatsapp": "https://api.whatsapp.com/send?phone=258862840075",
    "Facebook": "Zëüs Lykraios Takashi",
    "YouTube":  "Tina Bot conteudos",
    "Canal do WhatsApp":  "https://whatsapp.com/channel/0029VamcXnuFsn0ZotDz7c2A",
    "Instagram": "Tina_Conteudos",
  }
}}
    return jsonify(documentation)

# Rota para buscar o vídeo e gerar links de download
@app.route('/api/youtube/download', methods=['GET'])
def ytdownloader():
    query = request.args.get('query')  # Parâmetro de busca (nome da música)
    if not query:
        return jsonify({'error': 'O parâmetroQuery é Obrigatório'}), 400

    video_info = get_video_info(query)
    if video_info:
        return jsonify(video_info)
    else:
        return jsonify({'error': 'Video mao encontradotente outro termo'}), 404

if __name__ == '__main__':
    app.run(debug=True)
