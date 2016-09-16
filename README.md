# PeckerWriter
<h3><b>lineartestV3.py:(2016.09.16更新)</b></h3>
1.PosCaculator(pos,init,l)<p>
●Input:座標位置(list)、初始位置(list)、板子寬度(float)<br>
●Output:兩轉輪繩子的總長度(list)<br>
●Pseudocode:<br>
def PosCaculator(pos,init,l):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;mpos = pos + init #當前的位置必須加上初始位置(原點)的位移量<br>
    &nbsp;&nbsp;&nbsp;&nbsp;roll = (sqrt(X^2 + Y^2), sqrt((L-X)^2 + Y^2))<br>
    &nbsp;&nbsp;&nbsp;&nbsp;return roll<br>

