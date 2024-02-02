import requests
from bs4 import BeautifulSoup

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


if response.status_code == 200:

    html_content = response.text
    
    soup = BeautifulSoup(html_content, 'html.parser')

    top_ranking_tables = soup.find_all('table', class_='top-ranking-table')

    print(graph_start)
    
    for top_ranking_table in top_ranking_tables:
            # Itera sobre as linhas da tabela
            for row in top_ranking_table.find_all('tr'):
                
                cells = row.find_all('td')

                # Verifica se há pelo menos três células antes de extrair
                if len(cells) >= 3:
                    # Extrai e imprime o texto das três primeiras células

                    Rank = cells[0].get_text().strip()
                    
                    title_h3 = cells[1].find('h3')
                    title = title_h3.get_text().strip() if title_h3 else "TITULO"

                    Score = cells[2].get_text().strip()

                    print(f'{Colors.YELLOW}{Rank:<4} {Colors.PURPLE}{title:<60} {Colors.GREEN}{Score} {Colors.RESET}')

    print(graph_end)                

else:
    print(f'Erro ao acessar a página. Código de status: {response.status_code}')
