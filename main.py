from fastapi import FastAPI
from jamo import j2hcj, h2j
from pydantic import BaseModel

# Fastapi 앱 생성
app = FastAPI(
    title="획 궁합 API",
    description=".",
)

# 모델 생성
class NameRequest(BaseModel):
    name1: str
    name2: str

# 자음/모음 -> 획 수
h_to_n = {
    'ㄱ': 2,
    'ㄴ': 2,
    'ㄷ': 3,
    'ㄹ': 5,
    'ㅁ': 4,
    'ㅂ': 4,
    'ㅅ': 2,
    'ㅇ': 1,
    'ㅈ': 3,
    'ㅊ': 4,
    'ㅋ': 3,
    'ㅌ': 4,
    'ㅍ': 4,
    'ㅎ': 3,
    'ㅏ': 2,
    'ㅑ': 3,
    'ㅓ': 2,
    'ㅕ': 3,
    'ㅗ': 2,
    'ㅛ': 3,
    'ㅜ': 2,
    'ㅠ': 3,
    'ㅡ': 1,
    'ㅣ': 1,
    'ㅐ': 3,
    'ㅒ': 4,
    'ㅔ': 3,
    'ㅖ': 4,
}

# 궁합 계산기
def calc_match(name: str) -> int:
    if len(name) is not 6: return -1
    cn = []

    # 획 개수로 변환
    for c in list(name): # 가나다 -> ['가', '나', '다']
        sum = 0
        js = j2hcj(h2j(c)) # 자소 문자로 변경
        for h in js:
            sum += h_to_n[h]
        cn.append(sum)

    # 더하기
    while len(cn) > 2:
        n_cn = []
        for i in range(len(cn)-1):
            n_cn.append((cn[i]+cn[i+1])%10)
        cn = n_cn

    # 퍼센트으로 변환
    if cn[0] == 0 and cn[1] == 0: return 100
    return cn[0]*10 + cn[1]

# 이름1과 이름2을 섞어주는 함수
def mix_names(name1: str, name2: str) -> str:
    result = ''
    for i in range(3):
        result += name1[i] + name2[i]
    return result

# 궁합 계산을 API로
@app.post('/')
def calc_percentage(req: NameRequest):
    mixed_name = mix_names(req.name1, req.name2)
    return {'percentage': calc_match(mixed_name)}