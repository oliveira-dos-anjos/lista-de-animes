import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request


# códigos para cores
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"

graph_start = f'{Colors.CYAN}{'='*70}{Colors.RESET}'
graph_end = f'{Colors.CYAN}{'='*70}{Colors.RESET}'

# URL da página
url = 'https://myanimelist.net/topanime.php'
response = requests.get(url)


def obter_lista_animes():

    if response.status_code == 200:

        html_content = response.text    
        
        soup = BeautifulSoup(html_content, 'html.parser')

        top_ranking_tables = soup.find_all('table', class_='top-ranking-table')

        lista_anime = []
        for top_ranking_table in top_ranking_tables:
            for row in top_ranking_table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 3:
                    Rank = cells[0].get_text().strip()
                    title_h3 = cells[1].find('h3')
                    title = title_h3.get_text().strip() if title_h3 else "TITULO"
                    Score = cells[2].get_text().strip()
                    lista_anime.append({'rank': Rank, 'title': title, 'score': Score})

        return lista_anime[1:]

    else:
        return [{'rank': '', 'title': 'Erro de Requisição', 'score': ''}]

# Criação da instância do Flask
app = Flask(__name__)

# Rota para a página inicial
@app.route('/')
def home():
    # Chama a função para obter a lista de animes
    lista_animes = obter_lista_animes()

    # Renderiza o template HTML e passa a lista de animes como contexto
    return render_template('index.html', lista_animes=lista_animes)

    # Retorna uma mensagem ou redireciona para outra página
    return "Lista de animes exibida no console."

# Inicia o aplicativo Flask
if __name__ == "__main__":
    app.run(debug=True)