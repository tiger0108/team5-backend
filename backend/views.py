import requests
import json
from django.http import JsonResponse
from django.shortcuts import render
from .tools import haversine

user_latitude = 35.0
user_longitude = 140.0

def get_hotels(request):
    # 楽天トラベルAPIのエンドポイント
    api_url = 'https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426'

    # 楽天APIキー
    api_key = '1029895826722862188'  # 自分のAPIキー

    params = {
        'format': 'json',
        'latitude': user_latitude,
        'longitude': user_longitude,
        'searchRadius': 3.0,
        'applicationId': api_key,
        'datumType': 1,
    }

    try:
        # APIリクエストを送信
        response = requests.get(api_url, params=params)

        # APIリクエストが失敗した場合のエラーハンドリング
        if response.status_code != 200:
            return JsonResponse({'error': f'API request failed with status code {response.status_code}'}, status=500)

        # レスポンスのデータを抽出
        hotels_list = response.json().get('hotels', [])
        if not hotels_list:
            return JsonResponse({'error': 'No hotels data found'}, status=500)

        hotels_response = []
        for hotels_info in hotels_list:
            hotel = hotels_info.get('hotel', [])
            hotelBasicInfo = hotel[0].get('hotelBasicInfo', {})

            # ホテルの緯度と経度を取得し、ユーザーの位置との距離を計算
            hotel_latitude = float(hotelBasicInfo.get('latitude', 0))
            hotel_longitude = float(hotelBasicInfo.get('longitude', 0))
            distance = haversine(user_latitude, user_longitude, hotel_latitude, hotel_longitude)

            # ホテル情報を 'hotel' キーでラップし、距離も追加
            hotel_info = {
                'hotelNo': hotelBasicInfo.get('hotelNo'),
                'hotelName': hotelBasicInfo.get('hotelName'),
                'hotelLatitude': hotelBasicInfo.get('latitude'),
                'hotelLongitude': hotelBasicInfo.get('longitude'),
                'distance': distance, 
                'telephone': hotelBasicInfo.get('telephoneNo'),
                'address': hotelBasicInfo.get('address1', '') + hotelBasicInfo.get('address2', ''),
                'URL': hotelBasicInfo.get('hotelInformationUrl'),
            }

            # 各ホテルの情報を 'hotel' キーで追加
            hotels_response.append({'hotel': hotel_info})

        # 全体を 'hotels' でラップしてレスポンス
        result = {
            'hotels': hotels_response
        }
        
        # 日本語のエンコーディングをUTF-8に設定
        json_response = JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})
        json_response['Content-Type'] = 'application/json; charset=utf-8'
    
        return json_response

    except Exception as e:
        # 例外が発生した場合のエラーハンドリング
        return JsonResponse({'error': str(e)}, status=500)

# def show_hotels(request):
#     return render(request, 'hotelapp/hotels.html')
