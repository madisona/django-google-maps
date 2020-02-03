``django-google-maps``\ 는 Django 버전 1.11+에서 Django 모델 용 V3 API에
대한 기본 훅을 제공하는 간단한 애플리케이션입니다.

``django-google-maps`` 버전 (0.7.0)부터는 Django가 위젯 템플릿 렌더링
시스템을 변경했기 때문에 Django 1.11+가 필요합니다. 버전 0.8.0은 Django
2.0+를 지원하며 Python 2.7 지원을 제거합니다.

저는 관리자 패널의 누군가가 자유 형식 주소를 입력하고, 주소가
변경되고지도 상에 그려 지도록 허용하고 있습니다. 위치가 100 % 정확하지
않은 경우 사용자는 마커를 올바른 지점으로 드래그 할 수 있으며 지리적
좌표가 업데이트됩니다.

상태
---

|Build Status|

용법:
-----

-``settings.py``\ 에\ ``django_google_maps`` 앱을 포함 시키십시오. -
Google Maps API 키를\ ``settings.py``\ 에 ’GOOGLE_MAPS_API_KEY\` (으)로
추가하십시오. - 주소 필드와 위치 정보 필드가 모두있는 모델을 만듭니다.

.. code:: python

    from django.db import models
    from django_google_maps import fields as map_fields

    class Rental(models.Model):
        address = map_fields.AddressField(max_length=200)
        geolocation = map_fields.GeoLocationField(max_length=100)

-``admin.py``\ 에 다음을 formfield_override로 포함하십시오.

.. code:: python

   from django.contrib import admin
   from django_google_maps import widgets as map_widgets
   from django_google_maps import fields as map_fields

   class RentalAdmin(admin.ModelAdmin):
       formfield_overrides = {
           map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
       }

-지도 유형 (기본적으로\ ``hybrid ')을 변경하려면,``\ AddressField\`
위젯에 html 속성을 추가 할 수 있습니다. 허용되는 값 목록은 ‘하이브리드’,
‘로드맵’, ‘위성’, ’지형’입니다.

.. code:: python

     from django.contrib import admin
     from django_google_maps import widgets as map_widgets
     from django_google_maps import fields as map_fields
     
     class RentalAdmin(admin.ModelAdmin):
         formfield_overrides = {
             map_fields.AddressField: {
               'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
         }

그게 당신이 시작하는 데 필요한 모든 것이어야합니다.

나는 또한 관리자가 읽기 전용으로 geolocation 필드를 만들어 사용자
(우연히)가 무의미한 값으로 변경하지 않도록하고 싶습니다. 입력란에 유효성
검사가 있으므로 잘못된 값을 입력 할 수는 없지만 의도 한 주소와 거의
일치하지 않는 내용을 입력 할 수 있습니다.

사용자에게 다시 주소를 표시 할 때 모델에 저장된 지오 코디네이터를
사용하여지도를 요청하십시오. 어쩌면 언젠가는 내가 그 모델을 구축 할
방법을 만들 수 있는지 살펴볼 것입니다.

.. |Build Status| image:: https://travis-ci.org/madisona/django-google-maps.png
   :target: https://travis-ci.org/madisona/django-google-maps