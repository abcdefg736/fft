
from math import pi , cos , sin , ceil , log

def fft ( p ) :

	"""
		Evaluates the polynomial p(x) of degree n-1 in the n nth roots of unity
		in O(n log n) time.

		It does so recursively by distributing the coefficients of p(x) over
		two polynomials of degree n/2-1. Suppose 2 divides n and let m = n / 2.
		Let
			p(x) = a_0 x^0 + a_1 x^1 + ... + a_{2m-1} x^{2m-1}
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

	# The recursion fairy evaluates u and v for us.
	fft( u )
	fft( v )

	# We will enumerate all the nth roots of unity starting with w = (-)1 and then
	# just multiplying w by the ( positive ) primitive nth root of unity z.
	w = complex( 1 )
	z = complex( cos( 2 * pi / n ) , sin( 2 * pi / n ) )

	# At each step of the loop we will yield p(w) and p(-w). There are m steps
	# times 2 roots which gives us 2m = n roots.
	for j in range ( m ) :

		p[   j   ] = u[j] + w * v[j]
		p[ m + j ] = u[j] - w * v[j]
		w *= z

def ifft ( array ) :

	n = len( array )

	if n == 1 : return

	m = n // 2

	u = [ array[   2 * j   ] for j in range( m ) ]
	v = [ array[ 2 * j + 1 ] for j in range( m ) ]

	ifft( u )
	ifft( v )

	w = complex( 1 )
	z = complex( cos( 2 * pi / n ) , - sin( 2 * pi / n ) )

	for j in range ( m ) :

		array[   j   ] = ( u[j] + w * v[j] ) / 2
		array[ m + j ] = ( u[j] - w * v[j] ) / 2
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

