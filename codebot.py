import sys
import StringIO
import contextlib
import time
import signal
from slackclient import SlackClient
from config import SLACK_API_KEY
# from RestrictedPython import compile_restricted
# from RestrictedPython.Guards import safe_builtins
#
# restricted_globals = dict(__builtins__=safe_builtins)

CHANNEL = 'D0ZCM2CJ1'
sc = SlackClient(SLACK_API_KEY)


@contextlib.contextmanager
def stdout_io():
    old = sys.stdout
    stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def signal_handler(signum, frame):
    raise Exception('End of Time')


def handle_request(action):
    if action.get('type') != 'message' or action.get('user') == 'U0ZCL04R5' or action.get('hidden'):
        return
    print(action)
    with stdout_io() as s:
        try:
            code = compile(action['text'], '<string>', 'exec')
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(5)
            exec code  # in restricted_globals
            signal.alarm(0)
            output = s.getvalue()
        except:
            output = sys.exc_info()
            sc.rtm_send_message(CHANNEL, "```{}\n{}```".format(output[0], output[1]))
            return
    if output:
        sc.rtm_send_message(CHANNEL, "```{}```".format(output))
    else:
        sc.rtm_send_message(CHANNEL, ':thumbsup:')


if __name__ == '__main__':
    if sc.rtm_connect():
        while True:
            action = sc.rtm_read()
            if action:
                handle_request(action[0])
            time.sleep(1)
    else:
        print('Connection Failed, invalid token?')
