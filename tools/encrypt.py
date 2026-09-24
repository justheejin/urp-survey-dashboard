"""대시보드 HTML을 팀 비밀번호로 암호화해 index.html(잠금 페이지)로 만든다.

사용법: URP_DASH_PW='비밀번호' python3 tools/encrypt.py <대시보드.html> index.html
비밀번호는 저장소에 절대 커밋하지 않는다.
"""
import base64, hashlib, hmac, json, os, secrets, subprocess, sys

ITER = 310000
src, out = sys.argv[1], sys.argv[2]
pw = os.environ['URP_DASH_PW'].encode()
plain = open(src, 'rb').read()

salt, iv = secrets.token_bytes(16), secrets.token_bytes(16)
dk = hashlib.pbkdf2_hmac('sha256', pw, salt, ITER, 64)
ek, mk = dk[:32], dk[32:]
ct = subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-K', ek.hex(), '-iv', iv.hex()],
                    input=plain, capture_output=True, check=True).stdout
tag = hmac.new(mk, iv + ct, hashlib.sha256).digest()

back = subprocess.run(['openssl', 'enc', '-d', '-aes-256-cbc', '-K', ek.hex(), '-iv', iv.hex()],
                      input=ct, capture_output=True, check=True).stdout
assert back == plain, 'round-trip failed'

b64 = lambda b: base64.b64encode(b).decode()
payload = json.dumps({'v': 1, 'iter': ITER, 'salt': b64(salt), 'iv': b64(iv), 'tag': b64(tag), 'ct': b64(ct)})
tpl = open(os.path.join(os.path.dirname(__file__), 'lock_template.html'), encoding='utf-8').read()
assert tpl.count('__PAYLOAD__') == 1
open(out, 'w', encoding='utf-8').write(tpl.replace('__PAYLOAD__', payload))
print(f'encrypted {len(plain)} bytes -> {out}')
