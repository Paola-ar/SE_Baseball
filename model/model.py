import networkx as nx
from networkx.classes import neighbors

from database.dao import DAO
import copy


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.teams = []
        self.team_map = {}
        self.mappa_salari = {}
        self.K = 3

    def get_anni(self):
        anni = DAO.anni_dd()
        return anni

    def load_teams(self,year):
        self.teams = DAO.get_teams_by_year(year)
        return self.teams

    def build_grafo(self,year):
        self.grafo.clear()
        self.mappa_salari = DAO.get_team_salary(year)

        #importante
        for i,t1 in enumerate(self.teams):
            for t2 in self.teams[i+1:]:
                w = self.mappa_salari.get(t1.id, 0) + self.mappa_salari.get(t2.id, 0)
                self.grafo.add_edge(t1, t2, weight=w)

        # creo la mappa id per recuperare nomi dei team
        self.team_map = {t.id: t for t in self.teams}

    def get_neighbors(self,team_node):
        vicini = []
        for n in self.grafo.neighbors(team_node):
            #team node = nodo iniziale trasmesso, n ogni suo vicino
            w = self.grafo[team_node][n]['weight']
            vicini.append((n,w))
        return sorted(vicini, key=lambda x:x[1], reverse=True)

    def compute_best_path(self,start):
        self.best_path = []
        self.best_weight = 0
        self._ricorsione([start],0,float("inf"))
        return self.best_path, self.best_weight

    def _ricorsione(self,path,weight, last_edge_weight):# archi con peso minore dell'arco usato
        last = path[-1]
        if weight > self.best_weight:
            self.best_weight = weight
            self.best_path = path.copy()

        vicini = self.get_neighbors(last)
        neighbors = []
        counter = 0
        for node, edge_w in vicini:
            if node in path:
                continue
            if edge_w <= last_edge_weight:
                neighbors.append((node,edge_w)) # vicini possibili con peso minore di quello precedente
                # li aggiungo ai vicini e ho aggiunto un arco, counter +=1
                counter += 1
                if counter >= self.K:
                    break

        for node,edge_w in neighbors: # tra tutti i vicini trovati li aggiungo al cammino
            path.append(node) # aggiungo solo il nodo trovato come vicino
            self._ricorsione(path,weight + edge_w,edge_w)
            path.pop()




