from fishingbot import FishingBot
from puzzle import PuzzleBot
from interface import PyWindow
import FreeSimpleGUI as sg

window = PyWindow().window
fishbot = FishingBot()
puzzleBot = PuzzleBot()

while True:

    event, values = window.read(timeout=1)
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break

    if event != sg.TIMEOUT_KEY:
        if event == '-BUTTONSTART-':
            fishbot.set_to_begin(values)
            fishbot.botting = not fishbot.botting
            puzzleBot.botting = False
        if event == '-BUTTONPUZZLESTART-':
            if puzzleBot.botting:
                puzzleBot.botting = False
            else:
                try:
                    puzzleBot.set_to_begin(values)
                except (FileNotFoundError, ValueError) as error:
                    sg.popup_error(str(error))
                    continue
                puzzleBot.botting = True
            fishbot.botting = False

    if fishbot.botting:
        fishbot.runHack()
        window['-BUTTONSTART-'].update('STOP')
    else:
        window['-BUTTONSTART-'].update('START')

    if puzzleBot.botting:
        try:
            puzzleBot.runHack()
            window['-BUTTONPUZZLESTART-'].update('STOP')
        except:
            puzzleBot.botting = not puzzleBot.botting
            fishbot.botting = False

    else:
        window['-BUTTONPUZZLESTART-'].update('START')

window.close()
