
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

		array[   j   ] = u[j] + w * v[j]
		array[ m + j ] = u[j] - w * v[j]
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

		array[   j   ] = 2 * ( u[j] + w * v[j] )
		array[ m + j ] = 2 * ( u[j] - w * v[j] )
		w *= z

def mul ( p , q ) :

	m = len( p )
	n = len( q )

	k = 2 ** ceil( log( m + n ) )

	u = p + [ complex( ) ] * ( k - m )
	v = q + [ complex( ) ] * ( k - n )

	forward( u )
	forward( v )

	r = [ u[j] * v[j] for j in range( k ) ]

	backward( r )

	return r
