###############################################################
# ‘ункци€ get_cells создает массив из €чеек ноутбука дл€ дальнейшей работы
# ¬озвращает массив cells([code1, output1],...[codeN, outputN]) 
############################################################### 
from google.colab import _message

def get_cells(logs=False):
  # получаю содержимое ноутбука, включа€ метаданные с результатами выполнени€ €чеек в формате json
  nb = _message.blocking_request("get_ipynb", request="", timeout_sec=10)
  cells = []
  cellin, cellout = '', ''

  for cell in nb["ipynb"]["cells"]:
    # €чейки с кодом, которые запускали  
    if cell["cell_type"] == "code" and cell["source"][0] != "# <hide>\n" and 'executionInfo' in cell["metadata"].keys():  
      if cell["metadata"]["executionInfo"]["status"] == "ok":  # провер€ем, что €чейка выполнена (присутствует информаци€ о результатах выполнени€)
        # удал€ем из кода комментарии, обедин€ем список в строку и передаем в проверочную функцию
        cellin = "".join(list(map(lambda x: x.split("#")[0], cell["source"])))
        cellout = ''
        if cell["outputs"]: # €чейка с выводом
          if cell["outputs"][0]["output_type"] == "stream":
            cellout = "".join(cell["outputs"][0]["text"])
            # if logs:  print(cellout)
        cells.append([cellin, cellout])
  if logs:
      print(*['\nINPUT:\n'+c[0]+['\n\nOUTPUT:\n'+c[1], '\n\nNo OUTPUT\n'][len(c[1])==0] for c in cells], sep='\n')
  return cells

###############################################################
# ‘ункци€ check_cells провер€ет наличие признака в €чейке
# ¬озвращает найденные совпадени€ matches_in, matches_out 
############################################################### 

def check_cells__(cellin='', cellout='', reg_marker_in='', reg_marker_out='', logs=0):
  matches_in, matches_out = '', ''
  if reg_marker_in: matches_in = re.findall(reg_marker_in, cellin, re.MULTILINE)
  if reg_marker_out: matches_out = re.findall(reg_marker_out, cellout, re.MULTILINE)

  if reg_marker_in and reg_marker_out:
    if logs:  print('два маркера:', reg_marker_in and reg_marker_out)
    if matches_in and matches_out:
      return matches_in, matches_out
  else:
    if matches_in or matches_out:
      if logs:  print('найдено одно совпадение:', matches_in, matches_out)
      return matches_in, matches_out
    if logs:  print(cell["metadata"], cell["source"])
  return '', ''

# функци€ выводит €чейки, в которых есть совпадение
# с - номер совпадени€, n - номер €чейка (должны считатьс€ внешней функцией)
def show_result(c, n, cellin='', cellout='', matches_in='', matches_out=''):
  print('#####################################'+'#'*len(str(n)))
  print(f'###### совпадение {c} в €чейке {n} #######')
  print('#####################################'+'#'*len(str(n)))
  print(f'matches_in: {matches_in}\nmatches_out: {matches_out}')

  print('\nЌайдено совпадение в следующих €чейках:\n')
  print('CODE:')
  print(cellin)
  print('\nOUTPUT:')
  print(cellout)