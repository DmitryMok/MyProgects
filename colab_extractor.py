###############################################################
# ������� get_cells ������� ������ �� ����� �������� ��� ���������� ������
# ���������� ������ cells([code1, output1],...[codeN, outputN]) 
############################################################### 
from google.colab import _message

def get_cells(logs=False):
  # ������� ���������� ��������, ������� ���������� � ������������ ���������� ����� � ������� json
  nb = _message.blocking_request("get_ipynb", request="", timeout_sec=10)
  cells = []
  cellin, cellout = '', ''

  for cell in nb["ipynb"]["cells"]:
    # ������ � �����, ������� ���������  
    if cell["cell_type"] == "code" and cell["source"][0] != "# <hide>\n" and 'executionInfo' in cell["metadata"].keys():  
      if cell["metadata"]["executionInfo"]["status"] == "ok":  # ���������, ��� ������ ��������� (������������ ���������� � ����������� ����������)
        # ������� �� ���� �����������, ��������� ������ � ������ � �������� � ����������� �������
        cellin = "".join(list(map(lambda x: x.split("#")[0], cell["source"])))
        cellout = ''
        if cell["outputs"]: # ������ � �������
          if cell["outputs"][0]["output_type"] == "stream":
            cellout = "".join(cell["outputs"][0]["text"])
            # if logs:  print(cellout)
        cells.append([cellin, cellout])
  if logs:
      print(*['\nINPUT:\n'+c[0]+['\n\nOUTPUT:\n'+c[1], '\n\nNo OUTPUT\n'][len(c[1])==0] for c in cells], sep='\n')
  return cells

###############################################################
# ������� check_cells ��������� ������� �������� � ������
# ���������� ��������� ���������� matches_in, matches_out 
############################################################### 

def check_cells__(cellin='', cellout='', reg_marker_in='', reg_marker_out='', logs=0):
  matches_in, matches_out = '', ''
  if reg_marker_in: matches_in = re.findall(reg_marker_in, cellin, re.MULTILINE)
  if reg_marker_out: matches_out = re.findall(reg_marker_out, cellout, re.MULTILINE)

  if reg_marker_in and reg_marker_out:
    if logs:  print('��� �������:', reg_marker_in and reg_marker_out)
    if matches_in and matches_out:
      return matches_in, matches_out
  else:
    if matches_in or matches_out:
      if logs:  print('������� ���� ����������:', matches_in, matches_out)
      return matches_in, matches_out
    if logs:  print(cell["metadata"], cell["source"])
  return '', ''

# ������� ������� ������, � ������� ���� ����������
# � - ����� ����������, n - ����� ������ (������ ��������� ������� ��������)
def show_result(c, n, cellin='', cellout='', matches_in='', matches_out=''):
  print('#####################################'+'#'*len(str(n)))
  print(f'###### ���������� {c} � ������ {n} #######')
  print('#####################################'+'#'*len(str(n)))
  print(f'matches_in: {matches_in}\nmatches_out: {matches_out}')

  print('\n������� ���������� � ��������� �������:\n')
  print('CODE:')
  print(cellin)
  print('\nOUTPUT:')
  print(cellout)