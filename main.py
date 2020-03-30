import PySimpleGUI as sg
from state import State
from pickle import dump, load


def main():
    state = State()

    layout = [[sg.Button("Add person")],
              [sg.Button("Generate visualization")],
              [sg.Input(key="saveas", visible=False, enable_events=True),
               sg.FileSaveAs("Save to file", file_types=(("Save file", "*.ftr"),))],
              [sg.Input(key="openfile", visible=False, enable_events=True),
               sg.FileBrowse("Open file", file_types=(("Save file", "*.ftr"),))]]

    window = sg.Window("Family Tree", layout, size=(250, 150))
    children = []

    def update():
        for me, windo in children:
            options = ["--"] + [p.name for p in state.people if p is not me]
            windo["parent"](value=windo["parent"].get(), values=options)
            windo["parent2"](value=windo["parent2"].get(), values=options)

    while True:
        update()
        event, values = window.read(timeout=100)
        if event in (None, 'Quit'):
            break
        elif event == "Add person":
            person = state.add_person()
            win = sg.Window(f"Person {len(state.people)}", state.layout(person))
            win.finalize()
            children.append((person, win))
        elif event == "Generate visualization":
            state.visualize()
        elif event == "saveas":
            dump(state, open(values["saveas"], 'wb'))
        elif event == "openfile":
            if not values["openfile"]:
                continue
            state = load(open(values["openfile"], 'rb'))
            for _, w in children:
                w.close()
            children = []
            for i, person in enumerate(state.people):
                win = sg.Window(f"Person {i + 1}", state.layout(person))
                win.finalize()
                children.append((person, win))
            continue

        for i, (person, child) in enumerate(children):
            event, values = child.read(timeout=0)
            person.name = values["name"]
            try:
                person.birth_year = int(values["birth"])
            except ValueError:
                pass
            try:
                person.death_year = int(values["death"])
            except ValueError:
                pass
            person.gender = 'm' if values[0] else ('n' if values[1] else 'f')
            person.parent = state.by_name(values["parent"])
            person.parent2 = state.by_name(values["parent2"])
            if event in (None, "Quit"):
                for to_remove in state.remove_person(person):
                    for other, wind in children:
                        if other is to_remove:
                            wind.close()
                del children[i]

    window.close()
    for _, child in children:
        child.close()


if __name__ == '__main__':
    main()
