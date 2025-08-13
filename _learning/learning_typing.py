from typing import Generic, TypeVar, Callable, ParamSpec, Concatenate

P = ParamSpec('P')
R = TypeVar('R')

def decorator(param: int) -> Callable[[Callable[P, R]], Callable[Concatenate[str, P], R]]:
    def wrapper(func: Callable[P, R]) -> Callable[Concatenate[str, P], R]:
        def wrapper(val: str, *args: P.args, **kwargs: P.kwargs) -> R:
            print("Decorator called")
            return func(*args, **kwargs)
        return wrapper
    return wrapper

@decorator(1)
def my_func(): 
    pass

T = TypeVar('T', int, float)

class MyClass(Generic[T]):

    def __init__(self, value:T) -> None:
        self.value: T = value

    def __add__(self, other: 'MyClass[T]') -> T:
        return self.value + other.value

instance = MyClass(1)
instance2 = MyClass(2)

res = instance + instance2


if __name__ == "__main__":
    my_func("smth")