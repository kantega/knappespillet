from signal import signal, SIGINT

_interrupted = False


def _interrupt_handler(sig, frame):
    global _interrupted
    _interrupted = True


def handle_interrupts():
    signal(SIGINT, _interrupt_handler)


def is_interrupted():
    return _interrupted
