from numbers import Number


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other
    
    def __sub__(self, other):
        if isinstance(other,Polynomial):
            length = max(len(self.coefficients),len(other.coefficients))
            a = self.coefficients + (0,)*(length - len(self.coefficients))
            b = other.coefficients + (0,)*(length - len(other.coefficients))
            coefs = tuple(x - y for x,y in zip(a,
                                               b))
            return Polynomial(coefs)
        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] - other,) + self.coefficients[1:])
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Polynomial):
            return other - self
        elif isinstance(other, Number):
            return Polynomial((other,) + (0,) * self.degree()) - self
        else:
            return NotImplemented

    def __mul__(self,other):
        if isinstance(other,Polynomial):
            coefs = [0]*(self.degree() + other.degree() + 1)
            for i,a in enumerate(self.coefficients):
                for j,b in enumerate(other.coefficients):
                    coefs[i+j] += a*b
            return Polynomial(tuple(coefs))
        elif isinstance(other, Number):
            return Polynomial(tuple(a*other for a in self.coefficients))
        else:
            return NotImplemented
    def __rmul__(self,other):
        return self*other

    def __pow__(self,other):
        if isinstance(other,int):
            if other < 0:
                raise ValueError("Negative exponent not supported for polynomials.")
            coefs = (1,)
            for i in range(other):
                coefs = (Polynomial(coefs) * self).coefficients
            return Polynomial(coefs)
        else:
            return NotImplemented

    def __call__(self,other):
        if isinstance(other,(float,int)):
            result = 0
            for i in range(self.degree() + 1):
                x = other**i
                result += self.coefficients[i]*x
            return result
        else:
            return NotImplemented

    def dx(self):
        result = []
        for i in range(self.degree()):
            result.append((i+1)*self.coefficients[i+1])
        if not result : 
            result.append(0)
        return Polynomial(tuple(result))
    
def derivative(p):
    return p.dx()