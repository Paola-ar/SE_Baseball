import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        # self._selected_year = None
        # self._selected_team = None

    # def populate_dd_anno(self):
    #     years = self._model.get_all_years()
    #     self._view.dd_anno.options.clear()
    #     self._view.dd_anno.options.append(ft.dropdown.Option((str(y))) for y in years)
    #     self._view.update()
    #
    # def handle_year_selected(self,e):
    #     try:
    #         year = int(self._view.dd_anno.value)
    #     except ValueError:
    #         self._view.show_alert("Inserire un anno superiore al 1980")
    #         return
    #     self._selected_year = year
    #     teams = self._model.get_teams_by_year(year)
    #
    #     # area testo squadre
    #     self._view.txt_out_squadre.controls.clear()
    #     self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(teams)}"))
    #
    #     for t in teams:
    #         self._view.txt_out_squadre.controls.append(ft.Text(t))
    #
    #     # aggiorno dd squadre
    #     self._view.dd_squadra.options.clear()
    #     self._view.dd_squadra.options.append(ft.dropdown.Option.append(ft.dropdown.Option(t))for t in teams)
    #
    #     self._view.dd_squadra.value =None
    #     self._view.update()



    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        try:
            year = int(self._view.dd_anno.value)
        except ValueError:
            self._view.show_alert("Inserire un anno superiore al 1980")
            return

        self._model.build_graph(year)


    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        # TODO
        team_id = self._view.dd_squadra.value
        team = self._model.team_map.get(int(team_id)) # controlla se esiste
        if not team:
            self._view.show_alert("Squadra selezionata non valida")
        self._view.txt_risultato.controls.clear()
        for n,w in self._model.get_team_details(team):
            self._view.txt_risultato.controls.append(ft.Text(f"{n} - peso {w}"))

        self._view.update()

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        # TODO
        team_id = self._view.dd_squadra.value
        # start = None
        # for t in self._model.teams:
        #     if t.id == int(team_id):
        #         start = t
        #         break
        start = next(t for t in self._model.teams if t.id == int(team_id))

        path,weight = self._model.get_best_path(start)

        self._view.txt_risultato.controls.clear()
        for i in range (len(path)-1):
            w = self._model.G[path[i]][path[i+1]]["weight"]
            self._view.txt_risultato.controls.append(ft.Text(f"{path[i]} -> {path[i+1]} (peso {w})"))

        self._view.txt_risultato.controls.append(ft.Text(f"Peso totale: {weight}"))
        self._view.update()


    """ Altri possibili metodi per gestire di dd_anno """""
    # TODO
    def get_years(self):
        return self._model.get_all_years()

    def handle_year_change(self,e):
        year = int(self._view.dd_anno.value)
        teams = self._model.get_teams_by_year(year)

        self._view.txt_out_squadre.controls.clear()
        self._view.txt_out_squadre.controls.append(ft.Text(f"Numero squadre: {len(teams)}"))
        for t in teams:
            self._view.txt_out_squadre.controls.append(ft.Text(t)) #__str__

        self._view.dd_squadra.options = [ft.dropdown.Option(key=str(t.id),text=t) for t in teams]
        #key è lidentificatore univoco, usato per tìritrovare la squadra nel model
        # text t ciò che l'utente vede
        self._view.update()

