from .monads.either import DoEither, DoEitherN, Either  # noqa
from .monads.either import _ as _e  # noqa
from .monads.either import do as do_either  # noqa

right = Either.right
left = Either.left


from .monads.maybe import DoMaybe, DoMaybeN, Maybe  # noqa
from .monads.maybe import _ as _m  # noqa
from .monads.maybe import do as do_maybe  # noqa

maybe = Maybe.of
just = Maybe.just
nothing = Maybe.nothing()


from .monads.try_monad import Try  # noqa

try_of = Try.of


from .functors.function import (  # noqa
    Function,
    Function2,
    Function3,
    Function4,
    Provider,
)
from .streams.stream import stream, stream_of  # noqa

pynction0 = Provider.decorator
pynction1 = Function.decorator
pynction2 = Function2.decorator
pynction3 = Function3.decorator
pynction4 = Function4.decorator

__version__ = "0.4.0"
