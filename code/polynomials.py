
from math import pi , cos , sin , ceil , log

def forward ( array ) :

	n = len( array )

	if n == 1 : return

	m = n // 2

	u = [ array[   2 * j   ] for j in range( m ) ]
	v = [ array[ 2 * j + 1 ] for j in range( m ) ]

	forward( u )
	forward( v )

	w = complex( 1 )
	z = complex( cos( 2 * pi / n ) , sin( 2 * pi / n ) )

	for j in range ( m ) :

		array[   j   ] = ( u[j] + w * v[j] ) / 2
		array[ m + j ] = ( u[j] - w * v[j] ) / 2
		w *= z

def backward ( array ) :

	n = len( array )

	if n == 1 : return

	m = n // 2

	u = [ array[   2 * j   ] for j in range( m ) ]
	v = [ array[ 2 * j + 1 ] for j in range( m ) ]

	backward( u )
	backward( v )

	w = complex( 1 )
	z = complex( cos( 2 * pi / n ) , - sin( 2 * pi / n ) )

	for j in range ( m ) :

		array[   j   ] = ( u[j] + w * v[j] ) * 2
		array[ m + j ] = ( u[j] - w * v[j] ) * 2
		w *= z

def mul ( p , q ) :

	m = len( p )
	n = len( q )

	k = 2 ** ceil( log( m + n , 2 ) )

	u = p + [ complex( 0 ) ] * ( k - m )
	v = q + [ complex( 0 ) ] * ( k - n )

	forward( u )
	forward( v )

	r = [ u[j] * v[j] for j in range( k ) ]

	backward( r )

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

