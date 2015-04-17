
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

def fft ( array , l ) :

	n = len( array )

	if n == 1 : return

	m = n // 2

	u = [ array[   2 * j   ] for j in range( m ) ]
	v = [ array[ 2 * j + 1 ] for j in range( m ) ]

	fft( u , l - 1 )
	fft( v , l - 1 )

	w = 1

	for j in range ( m ) :

		array[   j   ] = ( u[j] + w * v[j] ) % p
		array[ m + j ] = ( u[j] - w * v[j] ) % p
		w *= Z[l]
		w %= p

def ifft ( array , l ) :

	n = len( array )

	if n == 1 : return

	m = n // 2

	u = [ array[   2 * j   ] for j in range( m ) ]
	v = [ array[ 2 * j + 1 ] for j in range( m ) ]

	ifft( u , l - 1 )
	ifft( v , l - 1 )

	w = 1

	for j in range ( m ) :

		array[   j   ] = N * ( u[j] + w * v[j] ) % p
		array[ m + j ] = N * ( u[j] - w * v[j] ) % p
		w *= _Z[l]
		w %= p

def mul3 ( first , second , third ) :

	m = len( first )
	n = len( second )
	o = len( third )

	l = ceil( log( m + n + o , 2 ) )
	k = 2**l

	u = first + [ 0 ] * ( k - m )
	v = second + [ 0 ] * ( k - n )
	w = third + [ 0 ] * ( k - o )

	fft( u , l - 1 )
	fft( v , l - 1 )
	fft( w , l - 1 )

	r = [ ( u[j] * v[j] * w[j] ) % p for j in range( k ) ]

	ifft( r , l - 1 )

	for i in range( k - 1 ) :

		if r[i] >= b :

			r[i+1] += r[i] // b
			r[i] = r[i] % b

	return r

def read ( string ) :

	return list( map( int , reversed( string ) ) )

def write ( array ) :

	return "".join( map( str , reversed( array ) ) )


def main ( first , second , third ) :

	first = read( first )
	second = read( second )
	third = read( third )

	print( "(%s) * (%s) * (%s) = %s" % ( write( first ) , write( second ) , write( third ) , write( mul3( first , second , third ) ) ) )

if __name__ == "__main__" :

	import sys
	main( *sys.argv[1:] )
