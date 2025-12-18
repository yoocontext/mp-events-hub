from dishka import Provider, Scope, provide

from faststream.rabbit import RabbitBroker

from seedwork.infra.rmq.event_map import event_queue_map
from seedwork.application.interface.event_bus import IEventBus
from seedwork.infra.event_bus.fs import FsEventBus

class EventBusProvider(Provider):
    @provide(scope=Scope.APP)
    def faststream_rmq(
        self,
        broker: RabbitBroker,
    ) -> IEventBus:
        return FsEventBus(
            _broker=broker,
            _event_queue_map=event_queue_map,
        )
