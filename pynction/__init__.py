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
pynction0.__doc__ = Provider.decorator.__doc__
pynction1 = Function.decorator
pynction1.__doc__ = Function.decorator.__doc__
pynction2 = Function2.decorator
pynction2.__doc__ = Function2.decorator.__doc__
pynction3 = Function3.decorator
pynction3.__doc__ = Function3.decorator.__doc__
pynction4 = Function4.decorator
pynction4.__doc__ = Function4.decorator.__doc__

from .version import __version__  # noqa
