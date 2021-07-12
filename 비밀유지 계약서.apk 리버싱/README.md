카카오톡방에서 해킹을 당했는데 apk파일을 분석해 주실 수 있냐는 분이 계셨다. <br><br>

도와주고 싶었다. <br><br>

비밀유지 계약서.apk라는 앱을 받았고 <br><br>

jadx에 올리니 난독화가 되어 있었다. <br><br>

<img src="https://github.com/kgyeongseong/Reversing/blob/main/%EB%B9%84%EB%B0%80%EC%9C%A0%EC%A7%80%20%EA%B3%84%EC%95%BD%EC%84%9C.apk%20%EB%A6%AC%EB%B2%84%EC%8B%B1/KakaoTalk_20210713_014800670.png?raw=true">

<br>
그래서 검색을 하다보니<br><br>

apk 압축을 풀어서 .dex 파일을 dex2jar를 이용해 .dex -> .jar로 변환하고 jd(java decompiler)를 이용하니 어느정도 난독화가 해제되어 분석이 가능해졌다. <br><br>

분석을 통해 결과를 도출하였다. <br><br>

악성코드 분석에 대해 관심이 생긴 것 같다.
