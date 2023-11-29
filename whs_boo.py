from boofuzz import *


def main():
    target_ip = "192.168.0.2" #ip set
    session = Session(
        target=Target(connection=TCPSocketConnection(target_ip, 80)),
        target=Target(connection=TCPSocketConnection(target_ip, 23000)),
        target=Target(connection=TCPSocketConnection(target_ip, 34567)),
        target=Target(connection=TCPSocketConnection(target_ip, 8899)),
        target=Target(connection=UDPSocketConnection(target_ip, 3702)),
        target=Target(connection=UDPSocketConnection(target_ip, 34568)),
        target=Target(connection=UDPSocketConnection(target_ip, 34569))
    )

    define_proto(session=session)

    session.fuzz()

def define_proto(session):
    print(session)

if __name__ == "__main__":
    main()
