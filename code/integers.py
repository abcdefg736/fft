
from math import pi , cos , sin , ceil , log

p = 337
z = 85
_z = 226
b = 10

x = 169
y = 2

def forward ( array ) :

	n = len( array )

	if n == 1 : return

	m = n // 2

	u = [ array[   2 * j   ] for j in range( m ) ]
	v = [ array[ 2 * j + 1 ] for j in range( m ) ]

	forward( u )
	forward( v )

	w = 1

	for j in range ( m ) :

		array[   j   ] = x * ( u[j] + w * v[j] ) % p
		array[ m + j ] = x * ( u[j] - w * v[j] ) % p
		w *= ( ( z ** ( 8 // n ) ) % p )
		w %= p

def backward ( array ) :

	n = len( array )

	if n == 1 : return

	m = n // 2

	u = [ array[   2 * j   ] for j in range( m ) ]
	v = [ array[ 2 * j + 1 ] for j in range( m ) ]

	backward( u )
	backward( v )

	w = 1

	for j in range ( m ) :

		array[   j   ] = y * ( u[j] + w * v[j] ) % p
		array[ m + j ] = y * ( u[j] - w * v[j] ) % p
		w *= ( ( _z ** ( 8 // n ) ) % p )
		w %= p

def mul ( first , second ) :

	m = len( first )
	n = len( second )

	k = 2 ** ceil( log( m + n , 2 ) )

	u = first + [ 0 ] * ( k - m )
	v = second + [ 0 ] * ( k - n )

	forward( u )
	forward( v )

	print( u )
	print( v )

	r = [ ( u[j] * v[j] ) % p for j in range( k ) ]

	print( r )

	backward( r )

	print( r )

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

	print( first , first.limbs )
	print( second , second.limbs )

	print( "(%s) * (%s) = %s" % ( first , second , first * second ) )

if __name__ == "__main__" :

	import sys
	main( *sys.argv[1:] )
