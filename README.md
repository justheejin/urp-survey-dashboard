# URP 설문 분석 대시보드

성균관대 융합연구학점제(URP) 팀의 설문 분석 대시보드입니다.

- 주소: https://justheejin.github.io/urp-survey-dashboard/
- 설문 응답 데이터는 암호화되어 있어, 팀에서 공유한 전용 링크(주소 뒤 `#키`)로만 열립니다.

## 갱신 방법

```bash
URP_DASH_PW='팀 키' python3 tools/encrypt.py <대시보드.html> index.html
git add index.html && git commit -m "대시보드 갱신" && git push
```

키는 저장소에 커밋하지 않습니다.
