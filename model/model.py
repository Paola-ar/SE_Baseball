import networkx as nx
from networkx.classes import neighbors

from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.teams = []
        self.team_salaries = {}
        self.K = 3
        self.team_map = {}

        self.best_path = []
        self.best_weight = 0




    def get_all_years(self):
        return DAO.get_all_years()

    def get_teams_by_year(self,year):
        self.teams = DAO.get_teams_by_year(year)
        return self.teams

    def build_graph(self,year):
        self.G.clear()
        self.team_salaries = DAO.get_team_salary(year)

        # teams = DAO.get_teams_by_year(year)
        # self.team_salaries = DAO.get_team_salary(year) # chiave = team code
        #
        # # aggiungo i nodi
        # self.G.add_nodes_from(teams) # equilavente se teams è una lista di stringhe,
        # #perchè di base puo aggiungere nodi con attributi
        # # for t in teams: self.G.add_node(t)
        #
        # #aggiungo le coppie pesate
        # for i in range (len(teams)):
        #     for j in range(i+1,len(teams)):
        #         team1 = teams[i] # team code
        #         team2 = teams[j] # team code
        #         peso = self.team_salaries[team1] + self.team_salaries[team2]
        #         self.G.add_edge(team1,team2,weight=peso)
        for i,t1 in enumerate (self.teams):
            for t2 in self.teams[i+1:]:
                w = self.team_salaries.get(t1.id,0) + self.team_salaries.get(t2.id,0)
                self.G.add_edge(t1,t2,weight=w)

        # mappa id -> >Team per recuperare i nomi
        self.team_map = {t.id: t for t in self.teams}

    def get_team_details(self,team):
        if team not in self.G:
            return []

        neighbors = []

        for n in self.G.neighbors(team):
            peso = self.G[team][n]['weight']
            neighbors.append((n,peso))

        neighbors.sort(key=lambda x:x[1], reverse = True)
        return neighbors

    def get_best_path(self,start_team):
        self.best_path = []
        self.best_weight = 0

        self._ricorsione([start_team],0,float("inf"))
        return self.best_path, self.best_weight

    def _ricorsione(self,path,peso_corr,last_weight):
        last = path[-1]
        if peso_corr > self.best_weight:
            self.best_weight = peso_corr
            self.best_path = path.copy()

        vicini = self.get_team_details(last)
        neighbors = []
        counter = 0
        for node, edge_w in vicini:
            if node in path:
                continue
            if edge_w <= last_weight:
                neighbors.append((node,edge_w))
                counter += 1
                if counter == self.K:
                    break

        for node,edge_w in neighbors:
            path.append(node)
            self._ricorsione(path,peso_corr+edge_w,edge_w)
            path.pop()


        # # archi adiacenti trovati
        # edges = []
        # for n in self.G.neighbors(current):
        #     if n not in path: # i nodi devono apparire una sola volta
        #         w = self.G[current][n]['weight']
        #         if last_weight is None or w < last_weight: # prendo il nodo solo se il peso e minore
        #             edges.append((n,w))
        # edges.sort(key=lambda x:x[1], reverse = True) # ordino per peso decrescente
        # edges = edges[:K] # prendo solo fino a fattori k
        #
        # for n,w in edges:
        #     path.append(n)
        #     self._ricorsione(path,peso_corr+w,w,n,K)
        #     path.pop()
        #






