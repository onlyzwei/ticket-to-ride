import networkx as nx
from typing import List, Tuple, Set

class Board:
    def __init__(self):
        """Inicializa o tabuleiro com as cidades e conexões a partir de arquivos."""
        self.graph = nx.Graph()
        self.cities_file = "util/cities.txt"
        self.edges_file = "util/edges.txt"

        self.cities = self._read_cities(self.cities_file)
        self._create_cities()
        self._create_connections(self.edges_file)
        # estado inicial do tabuleiro
        self.original_board = self.graph.copy()

    def _read_cities(self, cities_file: str) -> List[str]:
        """Lê as cidades do arquivo e retorna uma lista de cidades."""
        with open(cities_file, 'r') as file:
            cities = [line.strip() for line in file.readlines()]
        return cities

    def _read_edges(self, edges_file: str) -> List[tuple]:
        edges = []
        
        # Abrir o arquivo para leitura
        with open(edges_file, 'r') as file:
            for line in file:
                # Separar os valores por vírgula
                parts = line.strip().split(',')
                
                # Extrair os valores da linha
                city1 = parts[0]
                city2 = parts[1]
                weight = int(parts[2])  # O peso é um número inteiro
                colors = parts[3:]  # Os outros valores são as cores
                
                # Adicionar a tupla à lista de arestas
                edges.append((city1, city2, weight, colors))
        
        return edges

    def _create_cities(self) -> None:
        """Cria as cidades no tabuleiro."""
        for city in self.cities:
            self.graph.add_node(city)

    def _create_edge(self, city1: str, city2: str, weight: int, edge_colors: List[str]) -> None:
        """Cria uma conexão entre duas cidades."""
        if city1 in self.cities and city2 in self.cities:
            self.graph.add_edge(city1, city2, weight=weight, edge_colors=edge_colors)
    
    def _create_edges(self, edges: List[tuple]) -> None:
        """Cria várias conexões entre cidades.""" 
        for city1, city2, weight, edge_colors in edges:
            self._create_edge(city1, city2, weight, edge_colors)
    
    def _create_connections(self, edges_file: str) -> None:
        """Cria as conexões entre as cidades."""
        edges = self._read_edges(edges_file)
        self._create_edges(edges)

    def has_edge(self, city1: str, city2: str) -> bool:
        """Verifica se existe uma conexão entre duas cidades."""
        return self.graph.has_edge(city1, city2)

    def _get_edge_colors(self, city1: str, city2: str) -> List[str]:
        """Retorna as cores das conexões entre duas cidades."""
        return self.graph[city1][city2]['edge_colors']

    def _get_edge_weight(self, city1: str, city2: str) -> int:
        """Retorna o peso da conexão entre duas cidades."""
        return self.graph[city1][city2]['weight']
    
    def remove_connection(self, city1: str, city2: str, edge_color: str) -> None:
        """
        Remove a conexão entre duas cidades que tem a cor especificada.
        
        Args:
            city1: String representando a primeira cidade
            city2: String representando a segunda cidade
            edge_color: String representando a cor da conexão
            
        Raises:
            ValueError: Se a conexão não existir
        """
        if not self.has_edge(city1, city2):
            raise ValueError(f"Não existe conexão da {city1} para {city2}")
        
        colors = self._get_edge_colors(city1, city2)

        # se a conexão é cinza, aceita qualquer cor, se não, aceita apenas a cor especificada
        if "grey" in colors:
            self.graph.get_edge_data(city1, city2)['edge_colors'].remove("grey")
        else:
            if edge_color not in colors:
                raise ValueError(f"Não existe conexão da {city1} para {city2} com a cor {edge_color}")
            self.graph.get_edge_data(city1, city2)['edge_colors'].remove(edge_color)

        if len(self.graph.get_edge_data(city1, city2)['edge_colors']) == 0:
                self.graph.remove_edge(city1, city2)
        
    def get_edges(self):
        """
        Retorna uma lista de tuplas com todas as conexões existentes.
        
        Returns:
            Lista de tuplas no formato [(cidade1, cidade2)]
        """
        return self.graph.edges()

    def get_edge_colors(self, city1, city2):
        """
        Retorna as cores da conexão entre duas cidades.
        
        Args:
            city1: String representando a primeira cidade
            city2: String representando a segunda cidade
            
        Returns:
            Lista de cores da conexão
        """
        return self.graph.get_edge_data(city1, city2)['edge_colors']

    def get_edge_weight(self, city1, city2):
        """
        Retorna o peso da conexão entre duas cidades (ou seja, a distância).
        
        Args:
            city1: String representando a primeira cidade
            city2: String representando a segunda cidade
            
        Returns:
            Inteiro representando o peso da conexão
        """
        return self.graph.get_edge_data(city1, city2)['weight']
    
    def get_path_weight(self, city1, city2):
        """
        Retorna o peso do caminho mais curto entre duas cidades.
        
        Args:
            city1: String representando a primeira cidade
            city2: String representando a segunda cidade
            
        Returns:
            Inteiro representando o peso do caminho
        """
        return nx.dijkstra_path_length(self.graph, city1, city2)
    
    def get_nodes(self):
        """
        Retorna todos os nós do grafo.
        
        Returns:
            Lista de nós
        """
        return self.graph.nodes()

    def get_cities(self):
        """
        Retorna uma lista de todas as cidades restantes que podem ser viajadas.
        
        Returns:
            Lista de cidades
        """
        return self.graph.nodes()
    
    def get_adj_cities(self, city1):
        """
        Retorna uma lista de cidades adjacentes a uma cidade específica
        que ainda possuem conexões disponíveis.
        
        Args:
            city1: String representando a cidade

        Returns:
            Lista de cidades adjacentes
        """

        adj_cities = []
    
        edges_out = self.graph.edges(city1)
        
        # Para cada aresta que sai da cidade especificada
        for edge in edges_out:
            # A aresta é uma tupla (cidade_origem, cidade_destino)
            # Adiciona a cidade_destino à lista de cidades adjacentes
            adj_city = edge[1]
            adj_cities.append(adj_city)
        
        return adj_cities
        
    def has_path(self, city1, city2):
        """
        Verifica se existe um caminho entre duas cidades.
        
        Args:
            city1: String representando a primeira cidade
            city2: String representando a segunda cidade
            
        Returns:
            Boolean indicando se existe caminho
        """
        return nx.has_path(self.graph, city1, city2)
    
    def iter_edges(self):
        """
        Retorna um iterador sobre todas as conexões e seus dados.
        
        Returns:
            Iterador de conexões
        """
        return self.graph.edges(data=True)
        
class PlayerBoard(Board):
    """Cria um grafo personalizado para cada jogador representar seu progresso."""
    
    def __init__(self):
        """Inicializa o tabuleiro do jogador."""
        self.graph = nx.Graph()
    
    def add_edge(self, city1, city2, route_dist, color):
        """
        Adiciona uma conexão ao tabuleiro do jogador.
        
        Args:
            city1: String representando a primeira cidade
            city2: String representando a segunda cidade
            route_dist: Inteiro representando a distância da rota
            color: String representando a cor da conexão
        """
        if not self.graph.has_edge(city1, city2):
            # se existe uma conexão, então nao adicionam, pois o jogador não pode pegar as duas conexoes entre duas cidades
            self.graph.add_edge(city1, city2, weight=route_dist, edge_colors=[color])
        else:
            print(f"Conexão entre {city1} e {city2} já existe. Não é possível adicionar outra conexão entre as mesmas cidades.")

    def longest_path(self, start: str) -> Tuple[int, Tuple[List[str], Set[Tuple[str, str]]]]:
        """
        Encontra o caminho mais longo a partir de uma cidade inicial usando busca em profundidade (DFS).
        Retorna uma tupla: (peso_total, ([cidades_no_caminho], {arestas_usadas})).

        Args:
            start: Cidade inicial para começar a busca.

        Returns:
            Tupla no formato (peso_total, ([cidades_no_caminho], {arestas_usadas})).

        >>> p = PlayerBoard()
        >>> p.add_edge('a', 'b', 1, 'blue')
        >>> p.add_edge('b', 'd', 1, 'blue')
        >>> p.add_edge('d', 'e', 1, 'blue')
        >>> p.add_edge('e', 'f', 98, 'blue')
        >>> p.add_edge('e', 'b', 1, 'blue')
        >>> p.add_edge('b', 'c', 1, 'blue')
        >>> p.add_edge('a', 'z', 1, 'blue')
        >>> weight, (path, edges) = p.longest_path('b')
        >>> weight
        100
        >>> path
        ['b', 'd', 'e', 'f']
        >>> sorted(edges)
        [('b', 'd'), ('d', 'e'), ('e', 'f')]
        """
        best_weight = 0
        best_path = ([], set())  # ([cities], {edges})

        # Pilha para DFS: cada item é ([caminho atual], {arestas exploradas})
        stack = [([start], set())]

        while stack:
            current_path, explored_edges = stack.pop()

            # Calcula o peso do caminho atual, se houver arestas
            if explored_edges:
                current_weight = sum(self.get_edge_weight(u, v) for u, v in explored_edges)
                if current_weight > best_weight:
                    best_weight = current_weight
                    best_path = (current_path, explored_edges)

            # Última cidade do caminho atual
            last_city = current_path[-1]

            # Encontra vizinhos ainda não visitados por essa sequência de arestas
            for neighbor in self.get_adj_cities(last_city):
                edge = tuple(sorted([last_city, neighbor]))
                if edge not in explored_edges:
                    new_path = current_path + [neighbor]
                    new_explored_edges = explored_edges | {edge}
                    stack.append((new_path, new_explored_edges))

        return (best_weight, best_path)
