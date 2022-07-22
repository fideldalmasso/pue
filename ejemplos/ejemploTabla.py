import PySimpleGUI as sg
import random, string

# ------ Some functions to help generate data for the table ------
def word():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))
def number(max_val=1000):
    return random.randint(0, max_val)

def make_table(num_rows, num_cols):
    data = [[j for j in range(num_cols)] for i in range(num_rows)]
    data[0] = [word() for _ in range(num_cols)]
    for i in range(0, num_rows):
        data[i] = [i, word(), *[number() for i in range(num_cols - 1)]]
    return data

def main_example1():
    def edit_cell(location):
        layout = [[sg.In(s=5, k='-IN-')],
                  [sg.B('Ok', visible=False, bind_return_key=True)]]

        window = sg.Window('', layout, no_titlebar=True, location=location, margins=(0,0), element_padding=(0,0), return_keyboard_events=True, keep_on_top=True, modal=True)
        while True:
            event, values = window.read()
            print(event, values)
            if event == 'Ok':
                window.close()
                return values['-IN-']
            elif event.startswith('Escape'):
                window.close()
                return None

    # ------ Make the Table Data ------
    # sg.Print('Creating table...')
    data = make_table(num_rows=10_000, num_cols=6)
    # headings = [str(data[0][x])+'     ..' for x in range(len(data[0]))]
    headings = [f'Col {col}' for col in range(len(data[0]))]
    # sg.Print('Done creating table.  Creating GUI...')
    layout = [[sg.Table(values=data, headings=headings, max_col_width=25,
                        auto_size_columns=True,
                        # display_row_numbers=True,
                        justification='right',
                        num_rows=20,
                        alternating_row_color=sg.theme_button_color()[1],
                        key='-TABLE-',
                        # selected_row_colors='red on yellow',
                        # enable_events=True,
                        # select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                        expand_x=True,
                        expand_y=True,
                        enable_click_events=True,  # Comment out to not enable header and other clicks
                        )],
              [sg.Button('Read'), sg.Button('Double'), sg.Button('Change Colors')],
              [sg.Text('Cell clicked:'), sg.T(k='-CLICKED-')]]


    window = sg.Window('Table Element - Example 1', layout, resizable=True)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if isinstance(event, tuple):
            cell = event[2]
            window['-CLICKED-'].update(cell)
            new_value = edit_cell(location=window.mouse_location())
            if new_value is not None:
                data[cell[0]][cell[1]] = new_value
                window['-TABLE-'].update(data)

    window.close()

main_example1()

