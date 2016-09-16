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
2.DoRun(pos,init,l,init_pos):將筆架移動到指定位置中的函數(目前只用print)<p>
●Input:座標位置pos(list)、初始位置init(list)、板子寬度l(float)、經過座標運算的初始位置值init_pos(list)<br>
●Output:None<br>
●Pseudocode:<br>
def DoRun(pos,init,l,init_pos):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;roll = PosCaculator(pos,init,l)<br>
    &nbsp;&nbsp;&nbsp;&nbsp;pos_move = roll - init_pos #目標位置轉輪繩子長度減去初始位置轉輪繩子的長度即為兩步進馬達需要走的距離<br>
    &nbsp;&nbsp;&nbsp;&nbsp;使用pos_move的值傳送Gcode<br><p>
3.SliceMove(a,b,l,init,init_pos,Slice):使馬達以Slice單位一步步移動至目標位置<p>
●Input:兩點座標值a,b(list)、板子寬度l(float)、初始位置init(list)、經過座標運算的初始位置值init_pos(list)、移動單位Slice(float)<br>
●Output:None<br>
●Pseudocode:<br>
def SliceMove(a,b,l,init,init_pos,Slice):<br>
    &nbsp;&nbsp;&nbsp;&nbsp;V = b-a #求出a,b兩點的向量<br>
    &nbsp;&nbsp;&nbsp;&nbsp;dis_v = hypot(V[0],V[1])<br>
    &nbsp;&nbsp;&nbsp;&nbsp;if dis_v != 0: #有移動時<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;v = V/dis_v #V的單位向量:v = V/|V|<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;slice_v = Slice*v #求出slice vector<br>
        &nbsp;&nbsp;&nbsp;&nbsp;while dis_v > Slice:<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a = a + slice_v #移動一單位的slice vector<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DoRun(a,init,l,init_pos)<br>
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; dis_v = dis_v - Slice<br>
        &nbsp;&nbsp;&nbsp;&nbsp;if dis_v > 0: #假設Slice無法完整走完剩下的距離就直接走完<br>
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DoRun(b,init,l,init_pos)<br><p>

