def show_field(field):
    txt = ''
    for i in range(len(field)):
        if not i % 3:
            txt += f'\n{"-" * 25}\n'
        txt += f'{field[i]:^8}'
    txt += f"\n{'-' * 25}"
    return txt