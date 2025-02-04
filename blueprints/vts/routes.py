from itertools import combinations
import networkx as nx
from flask import Blueprint, render_template, request

# algorytm ze strony:
# https://iq.opengenus.org/algorithm-to-find-cliques-of-a-given-size-k/

def k_cliques(graph):
    # 2-cliques
    cliques = [{i, j} for i, j in graph.edges() if i != j]
    k = 2

    while cliques:
        maximal_cliques = cliques.copy()
        
        # merge k-cliques into (k+1)-cliques
        cliques_1 = set()
        for u, v in combinations(cliques, 2):
            w = u ^ v
            if len(w) == 2 and graph.has_edge(*w):
                cliques_1.add(tuple(u | w))
                # remove u and v, as we know they can't be maximal
                if v in maximal_cliques:
                    maximal_cliques.remove(v)
                if u in maximal_cliques:
                    maximal_cliques.remove(u)
        # result
        yield maximal_cliques

        # remove duplicates
        cliques = list(map(set, cliques_1))
        k += 1


def print_cliques(graph):
    global Roz
    Cliques =[]
    for cliques in k_cliques(graph):
        for clique in cliques:
            clique = [Roz[i] for i in clique]
            clique.sort(key=str.lower)
            Cliques.append(clique)
    return Cliques
            

def add_student_to_graph(student):
    global graph
    # zamienia nazwy rozszerzeń na indeksy
    student = [Roz.index(x) for x in student[2:]]
    # usuwa połączenia pomiędzy przedmiotami, które mają wspólnego ucznia
    for edge in list(combinations(student, 2)):
        try:
            graph.remove_edge(*edge)
        except:
            pass

def main(file):
    # czyta podany plik w formacie:
    # IMIĘ NAZWISKO ROZSZERZENIE ROZSZERZENIE ROZSZERZENIE
    # IMIĘ NAZWISKO ROZSZERZENIE ROZSZERZENIE ROZSZERZENIE
    # oddzielone tabami lub spacjami, rozszerzenia opisane pełnymi nazwami lub kodami (byle jednolicie w całym pliku)
    global Roz
    global graph

    Students = [line.split(",") for line in file.strip().split("\n")]
    # tworzy listę rozszerzeń
    Roz = Students.pop(0)
    # tworzy graf-klikę, w którym każdy przedmiot-wierzchołek jest połączony ze wszystkimi innymi
    nodes = len(Roz)
    graph = nx.Graph()
    graph.add_edges_from(list(combinations(range(nodes), 2)))
    # usuwa połączenia między przedmiotami, które mają wspólnego ucznia
    for student in Students:
        # print(student)
        add_student_to_graph(student)   
    # pokazuje, co wykminił
    response = print_cliques(graph)
    return response



vts = Blueprint('vts', __name__, template_folder='templates', static_folder='static')
active_tab = "vts"

@vts.route('/', methods=["POST", "GET"])
def vts_route():
    if request.method == "POST":
        req = request.get_json()
        file = req["data"]
        try:
            response = main(file)
        except:
            response = ["Niewłaściwy plik"]
        return response
    return render_template("vts.html", active_tab=active_tab)