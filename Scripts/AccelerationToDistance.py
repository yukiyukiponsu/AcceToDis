#外部ライブラリ使用
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from scipy.interpolate import interp1d

#サンプリング間隔 20ms
samplingTime = 0.02
#サンプリング周波数
#samplingRate = 1.0/samplingTime
print('AccelerationData CSVFileName')
fileName_acceleration = input('>>')
Acceleration = pd.read_csv(filepath_or_buffer= fileName_acceleration, encoding="utf8", sep=",")

y_array_Acceleration = Acceleration.iloc[:,1]
print("Androidのy軸加速度(重力成分なし)の出力")
print(y_array_Acceleration)
print("20msでリサンプルしたAndroidの数")
print(len(y_array_Acceleration))
AccelerationLength = len(y_array_Acceleration)

#加速度[m/s2]を速度[m/s]に台形積分を用いて変換
acceleration_velocity= [0]*AccelerationLength

for i in range(1, AccelerationLength):
    acceleration_velocity[i] = (((y_array_Acceleration[i] + y_array_Acceleration[i-1])*samplingTime)/2.0) + acceleration_velocity[i-1]

#print("加速度を速度に変換したときの値")
#print(acceleration_velocity)

#速度[m/s]を距離[m]に台形積分を用いて変換
acceleration_distance = [0]*AccelerationLength
for i in range(1, AccelerationLength):
     acceleration_distance[i] = (((acceleration_velocity[i] + acceleration_velocity[i-1])*samplingTime)/2.0) + acceleration_distance[i-1]

#print("速度を距離に変換したときの値")
#print(acceleration_distance)

#時間軸の初期化
time_array = [0]*AccelerationLength
for i in range(1, AccelerationLength):
    time_array[i] = 0.02*i

#始まりの時間
for i in range(0, 1):
    t_Min = time_array[i]
#print(x_Min)

#終わりの時間
for i in range(AccelerationLength-1, AccelerationLength):
    t_Masset = time_array[i]
#print(x_Masset)

#時間成分
t = np.linspace(t_Min, t_Masset, AccelerationLength)

#実際に計測した距離[m]
real_distance = 0.3

#全体の距離の合計を表示
print('\n全体の距離の合計値')
for i in range(AccelerationLength-1, AccelerationLength):
    print("距離の推定値[cm]")
    print(acceleration_distance[i]*100)

#誤差率の表示
print('\n測定した距離と理論的な距離の誤差率表示')
for i in range(AccelerationLength-1, AccelerationLength):
    data_acceleration_distance = acceleration_distance[i]

    error_upper = data_acceleration_distance - real_distance
    #print(error_upper)
    error_upper_abs = abs(error_upper)
    #print(error_upper_abs)
    error_lower = real_distance
    error_rate = (error_upper_abs/error_lower)*100

    print('誤差率 (%)')
    print("距離測定の誤差率")
    print(error_rate)

print("\nグラフ表示")
fig = plt.figure()
asset_Acceleration = fig.add_subplot(1,1,1)

print('加速度センサから得たデータ')
#ラベルの名前
asset_Acceleration.set_xlabel('time[s]')
asset_Acceleration.set_ylabel('value')
asset_Acceleration.set_title('Acce Veloc Meter') # グラフタイトル
# asset.set_aspect('equal') # スケールを揃える
#asset.grid()            # 罫線
#asset.set_xlim([-10, 10]) # x方向の描画範囲を指定
#asset.set_ylim([0, 1])    # y方向の描画範囲を指定
asset_Acceleration.plot(t, y_array_Acceleration, color="red", label="Accleration[m/s2]", linestyle = "solid")
asset_Acceleration.plot(t, acceleration_velocity, color="blue", label="Velocity[m/s]", linestyle = "dashed")
asset_Acceleration.plot(t, acceleration_distance, color="green", label="Meter[m]", linestyle = "dotted")
asset_Acceleration.legend(loc=0)    # 凡例

fig.tight_layout()  # レイアウトの設定
# plt.savefig('hoge.png') # 画像の保
plt.show() #グラフの表示
