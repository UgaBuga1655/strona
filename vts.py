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
            clique.sort()
            clique = "\t".join(clique)
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
            # print(f"Nie udało się usunąć krawędzi {edge}...")

def main(file):
    # czyta podany plik w formacie:
    # IMIĘ NAZWISKO ROZSZERZENIE ROZSZERZENIE ROZSZERZENIE
    # IMIĘ NAZWISKO ROZSZERZENIE ROZSZERZENIE ROZSZERZENIE
    # oddzielone tabami lub spacjami, rozszerzenia opisane pełnymi nazwami lub kodami (byle jednolicie w całym pliku)
    # input_file = sys.argv[1]
    global Roz
    global graph

    Students = [line.split() for line in file.strip().split("\n")]
    # tworzy listę rozszerzeń
    Roz = Students.pop(0)
    # for student in Students:
    #    for roz in student[2:]:
    #        if roz not in Roz:
    #            Roz.append(roz)

    # tworzy graf-klikę, w którym każdy przedmiot-wierzchołek jest połączony ze wszystkimi innymi
    nodes = len(Roz)
    graph = nx.Graph()
    graph.add_edges_from(list(combinations(range(nodes), 2)))
    # print(Roz)
    # usuwa połączenia między przedmiotami, które mają wspólnego ucznia
    for student in Students:
        add_student_to_graph(student)
    # print([e for e in graph.edges])    
    # pokazuje, co wykminił
    response = print_cliques(graph)
    return response



vts = Blueprint('vts', __name__, )
active_tab = "vts"

@vts.route('/')
def vts_route():
    return render_template("vts.html", active_tab=active_tab)

@vts.route("/file-submit", methods=["POST", "GET"])
def file_submit():
    if request.method == "GET":
        return render_template("file-submit.html", active_tab=active_tab)
    if request.method == "POST":
        file = request.form.get('dane')
        try:
            response = vts.main(file)
        except:
            response = ["Niewłaściwy plik"]
        return render_template("file-submit.html", response = response, active_tab=active_tab)
    
@vts.route("/editor")
def editor():
    return render_template("editor.html", active_tab=active_tab)