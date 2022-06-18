from .monads.either import DoEither  # noqa
from .monads.either import Either
from .monads.either import do as do_either  # noqa

right = Either.right
left = Either.left


from .monads.maybe import DoMaybe  # noqa
from .monads.maybe import Maybe  # noqa
from .monads.maybe import do as do_maybe  # noqa

maybe = Maybe.of
nothing: Maybe = Maybe.of(None)


from .monads.try_monad import Try  # noqa

try_of = Try.of


from .streams.stream import stream, stream_of  # noqa
