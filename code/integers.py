
from math import pi , cos , sin , ceil , log

b = 10

W = 16
p = 2**W+1

def inverse ( z , p ) :

	return z ** ( p - 2 ) % p

def generator ( p ) :

	for z in range ( 2 , p ) :

		w = z

		for k in range ( 2 , p - 1 ) :

			w *= z
			w %= p

			if w == 1 : break

		else : return z


z = generator( p )
_z = inverse( z , p )

N = inverse( 2 , p )

def table ( z , n ) :

	T = [ None ] * n

	T[n-1] = z

	for i in range( n-2 , -1 , -1 ) : T[i] = T[i+1] ** 2 % p

	return T

Z = table( z , W )
_Z = table( _z , W )

def forward ( array , l ) :

	n = len( array )

	if n == 1 : return

	m = n // 2

	u = [ array[   2 * j   ] for j in range( m ) ]
	v = [ array[ 2 * j + 1 ] for j in range( m ) ]

	forward( u , l - 1 )
	forward( v , l - 1 )

	w = 1

	for j in range ( m ) :

		array[   j   ] = ( u[j] + w * v[j] ) % p
		array[ m + j ] = ( u[j] - w * v[j] ) % p
		w *= Z[l]
		w %= p

def backward ( array , l ) :

	n = len( array )

	if n == 1 : return

	m = n // 2

	u = [ array[   2 * j   ] for j in range( m ) ]
	v = [ array[ 2 * j + 1 ] for j in range( m ) ]

	backward( u , l - 1 )
	backward( v , l - 1 )

	w = 1

	for j in range ( m ) :

		array[   j   ] = N * ( u[j] + w * v[j] ) % p
		array[ m + j ] = N * ( u[j] - w * v[j] ) % p
		w *= _Z[l]
		w %= p

def mul ( first , second ) :

	m = len( first )
	n = len( second )

	l = ceil( log( m + n , 2 ) )
	k = 2**l

	u = first + [ 0 ] * ( k - m )
	v = second + [ 0 ] * ( k - n )

	forward( u , l - 1 )
	forward( v , l - 1 )

	r = [ ( u[j] * v[j] ) % p for j in range( k ) ]

	backward( r , l - 1 )

	for i in range( k - 1 ) :

		if r[i] >= b :

			r[i+1] += r[i] // b
			r[i] = r[i] % b

	return r

def read ( string ) :

	return list( map( int , reversed( string ) ) )

def write ( array ) :

	return "".join( map( str , reversed( array ) ) )


class Integer ( object ) :

	def __init__ ( self , args ) :

		if isinstance ( args , str ) :

			self.limbs = read( args )

		else :

			self.limbs = args

	def __len__ ( self ) :

		return len( self.limbs )

	def __str__ ( self ) :

		return write( self.limbs )

	def __mul__ ( self , other ) :

		return Integer( mul( self.limbs , other.limbs ) )


def main ( first , second ) :

	first = Integer( first )
	second = Integer( second )

	print( "(%s) * (%s) = %s" % ( first , second , first * second ) )

if __name__ == "__main__" :

	import sys
	main( *sys.argv[1:] )
