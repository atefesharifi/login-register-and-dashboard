from django.core.cache import cache
from kavenegar import *
from redis.exceptions import ConnectionError as RedisServerConnectionError

KEY_KAVENEGAR = '4442494F6A77766776746B3444575466373961693741335956544F6B45683669556B6C7731493538534A413D'
SENDER = '1000596446'


def send_smd(code, phone):
    api = KavenegarAPI(KEY_KAVENEGAR)
    params = {'sender': SENDER, 'receptor': phone, 'message': "Use " + str(code) + " to login your account."}
    api.sms_send(params)


def set_otp_cache(team_id, code):
    try:
        cache.set(key=str(team_id), value={'code': str(code)}, timeout=50)
    except RedisServerConnectionError:
        raise RedisServerConnectionError
    return code
