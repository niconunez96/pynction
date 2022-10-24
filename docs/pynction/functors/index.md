# Module pynction.functors

## Sub-modules

- [pynction.functors.function](./function.md)

## Classes

`Functor(*args, **kwargs)`
: Abstract base class for generic types.

    A generic type is typically declared by inheriting from
    this class parameterized with one or more type variables.
    For example, a generic mapping type might be defined as::

      class Mapping(Generic[KT, VT]):
          def __getitem__(self, key: KT) -> VT:
              ...
          # Etc.

    This class can then be used as follows::

      def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
          try:
              return mapping[key]
          except KeyError:
              return default

    ### Ancestors (in MRO)

    * typing.Generic
    * typing_extensions.Protocol

    ### Descendants

    * pynction.functors.function.Function
    * pynction.functors.function.Function2
    * pynction.functors.function.Function3
    * pynction.functors.function.Function4
    * pynction.functors.function.Provider

    ### Methods

    `map(self, f: Callable[[+T_cov], ~T2]) ‑> pynction.functors.Functor[~T2]`
    :
