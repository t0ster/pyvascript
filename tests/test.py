from unittest import TestCase
from pyvascript.grammar import compile
from textwrap import dedent

class PyvaTest(TestCase):
    def check(self, source, result):
        source = dedent(compile(dedent(source))).strip()
        result = dedent(result).strip()
        try:
            self.assertEqual(source, result)
        except:
            raise AssertionError('\n%s\n!=\n%s' % (repr(source), repr(result)))

class Test(PyvaTest):
    def test_dot(self):
        self.check('x.y.z', 'x.y.z;')

    def test_getitem(self):
        self.check('x[0]', 'x[0];')
        self.check('x[0][bla]', 'x[0][bla];')

    def test_dot_getitem(self):
        self.check('x.y[0]', 'x.y[0];')
        self.check('x.y[0].z', 'x.y[0].z;')
        self.check('x.y[0].z[214]', 'x.y[0].z[214];')

    def test_call_dot_getitem(self):
        self.check('x.f().y[0]', 'x.f().y[0];')
        self.check('x.y[0].z()', 'x.y[0].z();')
        self.check('x.y[0].z[214].f().a', 'x.y[0].z[214].f().a;')

    def test_assign_call_dot_getitem(self):
        self.check('a = x.f().y[0]', 'a = x.f().y[0];')
        self.check('a = x.y[0].z()', 'a = x.y[0].z();')
        self.check('a = x.y[0].z[214].f().a', 'a = x.y[0].z[214].f().a;')
        self.check('a += x.y[0].z[214].f().a', 'a += x.y[0].z[214].f().a;')

    def test_if(self):
        self.check("""
        if a == 3 or b is None and c == True or d != False:
            f()
        """, """
        if ((((a == 3) || ((b === null) && (c == true))) || (d != false))) {
          f();
        }
        """)

    def test_while(self):
        self.check("""
        while a == 3 or b is None and c == True or d != False:
            f()
        """, """
        while ((((a == 3) || ((b === null) && (c == true))) || (d != false))) {
          f();
        }
        """)

    def test_for_range(self):
        self.check("""
        for i in range(10):
            f()
        """, """
        var _$tmp1_end = 10;
        for (i = 0; i < _$tmp1_end; i++) {
          f();
        }
        """)

        self.check("""
        for i in range(2, 10):
            f()
        """, """
        var _$tmp1_start = 2, _$tmp2_end = 10;
        for (i = _$tmp1_start; i < _$tmp2_end; i++) {
          f();
        }
        """)

        self.check("""
        for i in range(2, 10, 2):
            f()
        """, """
        var _$tmp1_start = 2, _$tmp2_end = 10, _$tmp3_step = 2;
        for (i = _$tmp1_start; i < _$tmp2_end; i += _$tmp3_step) {
          f();
        }
        """)

    def test_for_reversed_range(self):
        self.check("""
        for i in reversed(range(10)):
            f()
        """, """
        i = 10;
        while (i--) {
          f();
        }
        """)

        self.check("""
        for i in reversed(range(2, 10)):
            f()
        """, """
        var _$tmp1_start = (10) - 1, _$tmp2_end = 2;
        for (i = _$tmp1_start; i >= _$tmp2_end; i--) {
          f();
        }
        """)

        self.check("""
        for i in reversed(range(2, 10, 2)):
            f()
        """, """
        var _$tmp1_start = (10) - 1, _$tmp2_end = 2, _$tmp3_step = 2;
        for (i = _$tmp1_start; i >= _$tmp2_end; i -= _$tmp3_step) {
          f();
        }
        """)

    def test_for_in(self):
        self.check("""
        for i in x.y[10].z():
            f(i)
        """, """
        var _$tmp1_data = _$pyva_iter(x.y[10].z());
        var _$tmp2_len = _$tmp1_data.length;
        for (var _$tmp3_index = 0; _$tmp3_index < _$tmp2_len; _$tmp3_index++) {
          i = _$tmp1_data[_$tmp3_index];
          
          f(i);
        }
        """)
