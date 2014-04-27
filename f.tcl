
proc my_fun_1d {params} {
  set x1 [lindex $params 0]
  return [expr $x1*$x1 - 2*$x1]
}

proc my_fun_2d {params} {
  set x1 [lindex $params 0]
  set x2 [lindex $params 1]
  return [expr 2*$x1*$x1 + $x2*$x2]
}

set params [list]
while {[gets stdin line] >= 0} {
  lappend params $line
}

puts [my_fun_2d $params]
