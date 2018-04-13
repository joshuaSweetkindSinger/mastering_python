class Foo(object):
    def __init__(self, x, y, z):
        self._x = x # private
        self._y = y # private
        self.z  = z # public

    def bar(self):
        return self._x

    def _baz(self):
        return self._y


class VelocityMixin(object):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.velocity = 0


def make_class(base, mixin, seed):
    class new_class(mixin, base):
        def __init__(self, *args, **kwds):
            print("seed = ", seed)
            self.seed = seed
            super().__init__(*args, **kwds)

    return new_class


def doit():
    foo = make_class(Foo, VelocityMixin, 1)(1, 2, 3)
    y = foo.velocity
    print(y.velocity)
    print(y.seed)
    print(foo)

    bar = make_class(Foo, VelocityMixin, 2)(1, 2, 3)
    z = bar.velocity
    print(z.velocity)
    print(z.seed)
    print(bar)





if __name__ == '__main__':
    doit()
