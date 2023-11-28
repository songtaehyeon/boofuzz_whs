from boofuzz import *
from concurrent.futures import ThreadPoolExecutor  # 병렬 실행을 위한 모듈

def define_proto(session):
    # HTTP 프로토콜 정의
    req = Request("HTTP-Request", children=(
        Block("Request-Line", children=(
            Group(name="Method", values=["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE"]),
            Delim(name="space-1", default_value=" "),
            String(name="URI", default_value="/index.html"),
            Delim(name="space-2", default_value=" "),
            String(name="HTTP-Version", default_value="HTTP/1.1"),
            Static(name="CRLF", default_value="\r\n"),
        )),
        Block("Host-Line", children=(
            String(name="Host-Key", default_value="Host:"),
            Delim(name="space", default_value=" "),
            String(name="Host-Value", default_value="example.com"),
            Static(name="CRLF", default_value="\r\n"),
        )),
        Static(name="CRLF", default_value="\r\n"),
    ))
    session.connect(req)

def fuzz_session(session):
    # Boofuzz 세션을 실행하고 퍼징을 수행하는 함수
    session.fuzz()

if __name__ == "__main__":
    num_sessions = 3
    sessions = []

    # 병렬로 실행할 세션 생성 및 설정
    for rep in range(num_sessions):
        session = Session(
            target=Target(connection=TCPSocketConnection("127.0.0.1", 80)),
        )
        define_proto(session=session)
        sessions.append(session)

    # ThreadPoolExecutor를 사용하여 세션을 병렬로 실행
    with ThreadPoolExecutor(max_workers=num_sessions) as executor:
        executor.map(fuzz_session, sessions)
