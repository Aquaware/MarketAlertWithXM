import PySimpleGUI as sg

# 画面レイアウトを指定 ---- (*1)
layout = [
  [sg.Text('日給計算アプリ')],
  [sg.Text('開始時間', size=(15,1)), sg.InputText('09:00')],
  [sg.Text('終了時間', size=(15,1)), sg.InputText('17:00')],
  [sg.Text('休憩時間', size=(15,1)), sg.InputText('1:00')],
  [sg.Text('時給', size=(15,1)), sg.InputText('1100')],
  [sg.Submit(button_text='計算')]]

# イベントループ --- (*2)
win = sg.Window('日給計算', layout)
while True:
  event, values = win.read()
  if event is None: break
  if event == '計算':
    # ここで日給を計算
    sg.popup('ここで日給を計算')
    break