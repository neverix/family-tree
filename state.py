from dataclasses import dataclass
from typing import Optional
import PySimpleGUI as sg
import graphviz as gv


class State:
    def __init__(self):
        self.people = []

    def add_person(self):
        person = Person("", 1990, None, "n", None, None)
        self.people.append(person)
        return person

    def remove_person(self, person):
        to_close = []
        for other in self.people:
            if other.parent is person or other.parent2 is person:
                to_close.append(other)
                self.people.remove(other)
        self.people.remove(person)
        return to_close

    def by_name(self, name):
        for person in self.people:
            if person.name == name:
                return person
        return None

    def layout(self, person):
        return [
            [sg.Text("Name:"), sg.InputText(person.name, key="name")],
            [sg.Text("Birth Year:"), sg.InputText(person.birth_year, key="birth")],
            [sg.Text("Death Year:"), sg.InputText('' if person.death_year is None else person.death_year, key="death")],
            [sg.Text("Gender:"),
             sg.Radio("M", "gender", person.gender == 'm'),
             sg.Radio("N", "gender", person.gender == 'n'),
             sg.Radio("F", "gender", person.gender == 'f')],
            [sg.Text("Parent:"), sg.DropDown(["--"], "--" if person.parent is None else person.parent.name,
                                             key="parent", size=(20, 1))],
            [sg.Text("Parent 2:"), sg.DropDown(["--"], "--" if person.parent2 is None else person.parent2.name,
                                               key="parent2", size=(20, 1))]
        ]

    def visualize(self):
        graph = gv.Digraph()
        for i, person in enumerate(self.people):
            graph.node(str(i), f"{person.name}, {person.gender.upper()}\n"
                               f"{person.birth_year} - {person.death_year or 'current'}")
        for i, person in enumerate(self.people):
            if person.parent is not None:
                graph.edge(str(i), str(self.people.index(person.parent)))
            if person.parent2 is not None:
                graph.edge(str(i), str(self.people.index(person.parent2)))
        graph.render("out/graph.gv", view=True)


@dataclass
class Person:
    name: str
    birth_year: int
    death_year: Optional[int]
    gender: str
    parent: Optional["Person"]
    parent2: Optional["Person"]
