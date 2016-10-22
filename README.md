# PeckerWriter
<h3><b>簡易操作流程(2016.10.22更新)</b></h3><br>
ContourDetect.py(分析出輪廓)→CovertToBoard.py(座標轉換)→SendGcode.py(輸出)<br><br>
ContourDetect.py<br>
●Enter Img:(輸入圖片檔名)<br>
●File Save:(轉完座標檔檔名，存在gcode/Unajusted裡面)<br>
轉完後會出現Press <Enter> to terminate the prog..按下Enter後就會顯示輪廓分析的情形了<br>
<br>
ConvertToBoard.py<br>
●Enter:(Contour轉完座標檔檔名(gcode/Unajusted裡面))<br>
●Output:(轉完Gcode的檔名，存在gcode/裡)<br>
轉完後會出現Press <Enter> to terminate the prog..按下Enter後就會就轉完了<br>
<br>
SendGcode.py(建議不要在sublime REPL執行以免當掉)<br>
●Gcode:(gcode/裡的gcode指令檔)<br>
●step_port:(步進馬達的COM)<br>
●serv_port:(伺服馬達的COM)<br>
連接成功後會出現"Initialize grbl..."然後就會開始跑gcode，cmd裡面會顯示每行指令傳送的狀況，ok代表沒問題<br>
跑完後會出現Press <Enter> to terminate the prog..按下Enter後就會關掉COM並且顯示開始結束畫的時間<br>
<h3><b>簡易功能測試程式(2016.10.22更新)</b></h3><br>
TestCode/PenTest.py(提放筆測試)、TestCode/PosTest.py(測試馬達移動)
