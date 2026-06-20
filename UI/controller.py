import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def get_years(self):
        return self._model.get_anni()

    def handle_year_change(self,e):
        year = int(self._view.dd_anno.value)
        teams = self._model.load_teams(year)

        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(teams)}"))
        for t in teams:
            self._view.txt_out_squadre.controls.append(ft.Text(t))

        self._view.dd_squadra.options = [ft.dropdown.Option (key=str(t.id),text = t) for t in teams]
        self._view.update()

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        try:
            year = int(self._view.dd_anno.value)
        except ValueError:
            print(f"Selezionare un anno valido")
            return
        self._model.build_grafo(year)


    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO
        team_id = int(self._view.dd_squadra.value) # era stringa diventa intero
        # ho messo prima nel riempimento dropdown la stringa degli id con testo codice e nome

        self._view.txt_out_squadre.controls.clear()
        for n,w in self._model.get_neighbors(self._model.team_map[team_id]):
            self._view.txt_risultato.controls.append(ft.Text(f"{n} - peso {w}"))
        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO
        team_id = int(self._view.dd_squadra.value)
        start = self._model.team_map[team_id]
        path, weight = self._model.compute_best_path(start)

        self._view.txt_risultato.controls.clear()
        for i in range(len(path)-1):
            w = self._model.grafo[path[i]][path[i+1]]["weight"]
            self._view.txt_risultato.controls.append(ft.Text(f"{path[i]} -> {path[i+1]} (peso {w})"))
        self._view.txt_risultato.controls.append(ft.Text(f"Peso totale: {weight}"))
        self._view.update()

    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO