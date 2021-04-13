from collections.abc import Callable
from dataclasses import dataclass
from typing import Concatenate, Generic, Hashable, ParamSpec, TypeVar, TypeVarTuple

# Type Aliases
type TypeAlias[T: Hashable] = tuple[T, T]


def test_type_aliases() -> None:
    value: TypeAlias[int] = 1, 2
    assert value[0] == 1


def test_generic_functions() -> None:
    def type_hints() -> None:
        T = TypeVar("T")

        def identity(value: T) -> T:
            return value

        assert identity(1) == 1

    def type_parameter_syntax() -> None:
        def identity[T](value: T) -> T:
            return value

        assert identity(1) == 1

    type_hints()
    type_parameter_syntax()


def test_generic_classes() -> None:
    def type_hints() -> None:
        T = TypeVar("T")
        S = TypeVar("S")

        @dataclass
        class GenericClass(Generic[T, S]):
            t: T
            s: S

        instance: GenericClass[str, int] = GenericClass(t="1", s=1)
        assert instance.t == "1"
        assert instance.s == 1

    def type_parameter_syntax() -> None:
        @dataclass
        class GenericClass[T, S]:
            t: T
            s: S

        instance: GenericClass[str, int] = GenericClass(t="1", s=1)
        assert instance.t == "1"
        assert instance.s == 1

    type_hints()
    type_parameter_syntax()


def test_variadic_generic_classes() -> None:
    def type_hints() -> None:
        Ts = TypeVarTuple("Ts")

        @dataclass
        class VariadicGenericClass(Generic[*Ts]):
            args: tuple[*Ts]

            def __init__(self, *args: *Ts) -> None:
                self.args = args
                super().__init__()

        instance: VariadicGenericClass[str, int] = VariadicGenericClass("1", 1)

        arg0: str = instance.args[0]
        assert arg0 == "1"

        arg1: int = instance.args[1]
        assert arg1 == 1

    def type_parameter_syntax() -> None:
        @dataclass
        class VariadicGenericClass[*Ts]:
            args: tuple[*Ts]

            def __init__(self, *args: *Ts) -> None:
                self.args = args
                super().__init__()

        instance: VariadicGenericClass[str, int] = VariadicGenericClass("1", 1)

        arg0: str = instance.args[0]
        assert arg0 == "1"

        arg1: int = instance.args[1]
        assert arg1 == 1

    type_hints()
    type_parameter_syntax()


def test_param_spec() -> None:
    # Parameter specification variables are used to forward the parameter types
    # of one callable to another callable
    # They are only valid when used in Concatenate
    # or as the first argument to Callable,
    # or as parameters for user-defined Generics
    #
    # Concatenate adds, removes, or transforms parameters of another callable.

    def sum(x: int, y: int) -> int:
        return x + y

    def type_hints() -> None:
        P = ParamSpec("P")
        T = TypeVar("T")

        def identity(f: Callable[P, T]) -> Callable[P, T]:
            return f

        assert identity(sum)(1, 2) == 3

        def currying(f: Callable[Concatenate[int, P], T], value: int) -> Callable[P, T]:
            def function(*args: P.args, **kwargs: P.kwargs) -> T:
                return f(value, *args, **kwargs)

            return function

        assert currying(sum, 1)(2) == 3

    def type_parameter_syntax() -> None:
        def identity[**P, T](f: Callable[P, T]) -> Callable[P, T]:
            return f

        assert identity(sum)(1, 2) == 3

        def currying[
            **P, T
        ](f: Callable[Concatenate[int, P], T], value: int) -> Callable[P, T]:
            def function(*args: P.args, **kwargs: P.kwargs) -> T:
                return f(value, *args, **kwargs)

            return function

        assert currying(sum, 1)(2) == 3

    type_hints()
    type_parameter_syntax()
