import math

# ハバーサインの公式を使用して、2点間の距離を計算
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # 地球の半径（キロメートル）

    # 度をラジアンに変換
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c  # 距離を返す
