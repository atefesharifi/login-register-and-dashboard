from django.core.cache import cache
from kavenegar import *
from redis.exceptions import ConnectionError as RedisServerConnectionError

KEY_KAVENEGAR = '526339612F357834796D314D50586F51664674317A65642B6E4942575534385362754D6D486E396241454D3D'
SENDER = '1000596446'


def send_smd(code, phone):
    api = KavenegarAPI(KEY_KAVENEGAR)
    params = {'sender': SENDER, 'receptor': phone, 'message': "Use " + str(code) + " to login your account."}
    api.sms_send(params)


def set_otp_cache(team_id, code):
    try:
        # cache.set(key=str(team_id), value={'code': str(code)}, timeout=180)
        cache.set(key=str(team_id), value={'code': str(code)}, timeout=18000)
    except RedisServerConnectionError:
        raise RedisServerConnectionError
    return code
