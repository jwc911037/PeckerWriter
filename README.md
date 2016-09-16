# PeckerWriter
<h3><b>lineartestV3.py:(2016.09.16更新):測試座標轉換後的移動數據，並印出移動座標以及Gcode指令輸出的情形</b></h3>
1.PosCaculator(pos,init,l):進行垂直空間的座標轉換運算<p>
●Input:座標位置pos(list)、初始位置init(list)、板子寬度l(float)<br>
●Output:兩轉輪繩子的總長度(list)<br>
●Pseudocode:<br>
def PosCaculator(pos,init,l):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;mpos = pos + init #當前的位置必須加上初始位置(原點)的位移量<br>
    &nbsp;&nbsp;&nbsp;&nbsp;roll = (sqrt(X^2 + Y^2), sqrt((L-X)^2 + Y^2))<br>
    &nbsp;&nbsp;&nbsp;&nbsp;return roll<br><p>
2.DoRun(pos,init,l,init_pos):將筆架移動到指定位置中的函數(目前只用print)
●Input:座標位置pos(list)、初始位置init(list)、板子寬度l(float)、經過座標運算的初始位置值init_pos(list)<br>
●Output:None<br>
●Pseudocode:<br>
def DoRun(pos,init,l,init_pos):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;roll = PosCaculator(pos,init,l)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;pos_move = roll - init_pos #目標位置轉輪繩子長度減去初始位置轉輪繩子的長度即為兩步進馬達需要走的距離<br>
    &nbsp;&nbsp;&nbsp;&nbsp;使用pos_move的值傳送Gcode
