
from math import pi , cos , sin , ceil , log

def fft ( p ) :

	"""
		Evaluates the polynomial p(x) of degree n-1 in the n nth roots of unity
		in O(n log n) time.

		It does so recursively by distributing the coefficients of p(x) over
		two polynomials of degree n/2-1. Suppose 2 divides n and let m = n / 2.
		Let
			p(x) = a_0 x^0 + a_1 x^1 + a_2 x^2 + ... + a_{2m-1} x^{2m-1}
		then define
			u(x) = a_0 x^0 + a_2 x^1 + a_4 x^2 + ... + a_{2m-2} x^{m-1}
		and
			v(x) = a_1 x^0 + a_3 x^1 + a_5 x^2 + ... + a_{2m-1} x^{m-1}.
		u(x) and v(x) are both of degree m-1 and p(x) = u(x^2) + x v(x^2).

		Suppose our algorithm works, then we are able to evaluate u(x) and v(x) in the m mth
		roots of unity. To each mth root of unity z corresponds two nth roots of unity
		sqrt(z) and -sqrt(z). Hence we can evaluate p(x) for all nth roots of unity by
		letting
			p(sqrt(z)) = u(z) + sqrt(z) v(z)
		and
			p(-sqrt(z)) = u(z) - sqrt(z) v(z).

		When n = 1, p(x) = a_0 and evaluating it for any x yields a_0.

		The recurrence relation is T(n) = 2 T(n/2) + O(n) and by the master
		theorem: T(n) = O(n log n).
	"""

	# The polynomial p(x) is represented as a list of coefficients
	# [ a_0 , a_1 , ... , a_{n-1} ].
	# The size of this list is the number of coefficients.
	n = len( p )

	# We have seen that in the base case evaluating p(x) of degree 0 yields
	# a_0. For a polynomial of degree 0 we want its evaluation for the first
	# root of unity, i.e. 1, which is unique. We thus simply return a_0.
	if n == 1 : return

	# m is n divided by 2
	m = n // 2

	# We construct u(x) and v(x).
	u = [ p[   2 * j   ] for j in range( m ) ]
	v = [ p[ 2 * j + 1 ] for j in range( m ) ]

	# The recursion fairy evaluates u(x) and v(x) for us.
	fft( u )
	fft( v )

	# We will enumerate all the nth roots of unity starting with w = (-)1 and then
	# just multiplying w by a primitive nth root of unity z.
	w = complex( 1 )
	z = complex( cos( 2 * pi / n ) , sin( 2 * pi / n ) )

	# At each step of the loop we will yield p(w) and p(-w). There are m steps
	# times 2 roots which gives us 2m = n roots.
	for j in range ( m ) :

		p[   j   ] = u[j] + w * v[j]
		p[ m + j ] = u[j] - w * v[j]
		w *= z

	# Note that the output has the form
	# [ p(1) , p(z) , p(z^2) , ... , p(-1) , p(-z) , p(-z^2) , ... ]
	# which is equivalent to
	# [ p(z^0) , p(z^1) , p(z^2) , p(z^3) , ... , p(z^{n-1}) ]

def ifft ( p ) :

	"""
		Interpolates the n data points (x's are the nth roots of unity) in p by
		the polynomial p(x) of degree n-1 in O(n log n).

		It does so recursively by distributing the data points of p over
		two data sets of cardinality n/2-1. Suppose 2 divides n and let m = n / 2.
		Let z be a primitive nth root of unity.
		Let
			p = [ ( z^0 , y_0 ) , ( z^1 , y_1 ) , ... , ( z^{2m-1} , y_{2m-1} ) ]
		then define
			u = [ ( z^0 , y_0 ) , ( z^2 , y_2 ) , ... , ( z^{2m-2} , y_{2m-2} ) ]
		and
			v = [ ( z^0 , y_1 ) , ( z^2 , y_3 ) , ... , ( z^{2m-2} , y_{2m-1} ) ]
		u and v are both of cardinality m-1. Note that x's of u and v are the
		mth roots of unity.

		Suppose our algorithm works, then we are able to interpolate u and v by
		u(x) and v(x). We have
			u(z^0) = y_0
			u(z^2) = y_2
			u(z^4) = y_4
			...
		and
			v(z^0) = y_1
			v(z^2) = y_3
			v(z^4) = y_5
			...

		We can interpolate p for x's being the nth roots of
		unity by letting
			p_j = 1/2 ( u_j + v_j / z^j )
		and
			p_{m+j} = 1/2 ( u_j - v_j / z^j )
		because then

		- if j is even,
		p(z^j) = 1/2 u(z^j) * ( 1 + z^{jm}) + 1/2 sum ( v_j / z^i * z^{ji} ) ( 1 - z^{jm} )
		       = 1/2 u(z^j) * ( 1 + 1 ) + 1/2 sum ( v_j / z^i * z^{ji} ) ( 1 - 1 )
		       = u(z^j)
		       = y_j

		- if j is odd,
		p(z^j) = 1/2 u(z^j) * ( 1 + z^{jm}) + 1/2 sum ( v_i / z^i * z^{ji} ) ( 1 - z^{jm} )
		       = 1/2 u(z^j) * ( 1 - 1 ) + 1/2 sum ( v_i / z^i * z^{ji} ) ( 1 + 1 )
		       = 1/2 u(z^j) * ( 1 - 1 ) + 1/2 sum ( v_i * z^{(j-1)i} ) ( 1 + 1 )
		       = v(z^{j-1})
		       = y_j

		When n = 1, p_0 = y_0 because evaluating p(1) must yield y_0 while p
		has degree 0.

		Again, by the master theorem, T(n) = O(n log n).
	"""

	# The data points set p as a list of y_j values, x_j values are implicitely
	# assumed to be the n nth roots of unity [ z^0 , z^1 , ... , z^{n-1} ].
	# The size of this list is the number of data points.
	n = len( p )

	# In the case where there is only 1 data point we interpolate it using
	# p(x) = y_0, a constant function.
	if n == 1 : return

	# m is n divided by 2
	m = n // 2

	# We split p into u and v.
	u = [ p[   2 * j   ] for j in range( m ) ]
	v = [ p[ 2 * j + 1 ] for j in range( m ) ]

	# We let the recursion fairy interpolate u and v.
	ifft( u )
	ifft( v )

	# We will enumerate all the nth roots of unity inverses starting with w =
	# (-)1 and then just multiplying w by a primitive nth root
	# of unity inverse z.
	w = complex( 1 )
	z = complex( cos( 2 * pi / n ) , - sin( 2 * pi / n ) )
	#                                ^
	#                                |- inverse
	# ( cos + isin ) ( cos - isin ) = cos^2 + sin^2 = 1

	# This loop computes the n coefficients of p(x) in O(n) time.
	for j in range ( m ) :

		p[   j   ] = ( u[j] + w * v[j] ) / 2
		p[ m + j ] = ( u[j] - w * v[j] ) / 2
		w *= z

def mul ( p , q ) :

	m = len( p )
	n = len( q )

	k = 2 ** ceil( log( m + n , 2 ) )

	u = p + [ complex( 0 ) ] * ( k - m )
	v = q + [ complex( 0 ) ] * ( k - n )

	fft( u )
	fft( v )

	r = [ u[j] * v[j] for j in range( k ) ]

	ifft( r )

	return r

def read ( string ) :

	tokens = string.split( "+" )

	terms = [ ]

	for token in tokens :

		parts = map( int , token.split( "x^" ) )
		coefficient = complex( next( parts ) )
		exponent = next( parts , 0 )

		terms.append( ( coefficient , exponent ) )

	terms = sorted( terms , key = lambda t : t[1] )

	degree = terms[-1][1]

	coefficients = [ complex( 0 ) ] * ( degree + 1 )

	for coefficient , exponent in terms :

		coefficients[exponent] = coefficient

	return coefficients

def write ( array , e = 1e-6 ) :

	n = len( array )

	s = [ ]

	for i , a in enumerate( array ) :

		a = a.real

		if abs( a ) < e : continue

		elif not a : continue

		elif i == 0 : s.append( str( a ) )

		elif i == 1 : s.append( str( a ) + "x" )

		else : s.append( str( a ) + "x^" + str( i ) )

	return " + ".join( reversed( s ) )


class Polynomial ( object ) :

	def __init__ ( self , args ) :

		if isinstance ( args , str ) :

			self.coefficients = read( args )

		else :

			self.coefficients = args

	def __len__ ( self ) :

		return len( self.coefficients )

	def __str__ ( self ) :

		return write( self.coefficients )

	def __mul__ ( self , other ) :

		return Polynomial( mul( self.coefficients , other.coefficients ) )


def main ( p , q ) :

	p = Polynomial( p )
	q = Polynomial( q )

	print( "(%s) * (%s) = %s" % ( p , q , p * q ) )

if __name__ == "__main__" :

	import sys
	main( *sys.argv[1:] )

