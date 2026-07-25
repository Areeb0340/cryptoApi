from core.websocket_manager import WebSocketManager


class WebSocketPool:

    MAX_STREAMS_PER_SOCKET = 180

    def __init__(self):
        self.managers = []

    def create_pool(self, streams, base_url="wss://fstream.binance.com/public/stream"):

        self.managers.clear()
        batch = []

        for stream in streams:

            batch.append(stream)

            if len(batch) >= self.MAX_STREAMS_PER_SOCKET:

                manager = WebSocketManager(base_url=base_url)

                for s in batch:
                    manager.add_stream(s)

                self.managers.append(manager)
                batch = []

        if batch:

            manager = WebSocketManager(base_url=base_url)

            for s in batch:
                manager.add_stream(s)

            self.managers.append(manager)

    def get_managers(self):
        return self.managers

    @property
    def total_managers(self):
        return len(self.managers)

    @property
    def total_streams(self):
        return sum(len(manager.streams) for manager in self.managers)

    def summary(self):
        return {
            "managers": self.total_managers,
            "streams": self.total_streams,
            "average_streams": (
                round(self.total_streams / self.total_managers, 2)
                if self.total_managers
                else 0
            ),
        }
