/*
Amortization Schedule:

final month: a0*r + a0 == C

(a0+a1) * r + a1 == C
  ==>  (a0+a1) * r + a1 == a0*r + a0
  ==>  a1*r + a1 == a0 == a1 * (r+1)


(a0+a1+a2) * r + a2 == C
  ==>  (a0+a1+a2) * r + a2 == (a0+a1) * r + a1
  ==>  a2 * (r+1) == a1


1 + a^1 + a^2 + ... + a^(n-1) == S
  ==>
    a^1 + a^2 + ... + a^(n-1) + a^n == S*a
  ==>  1 - a^n == (1-a)*S
  ==>  S == (a^n - 1) / (a-1)

  a == 1/(r+1)

*/

package main

import (
	"fmt"
	"math"
)

func compound(n, r float64) float64 {
	a := 1.0 / (r + 1.0)
	return (a - 1) / (math.Pow(a, n) - 1.0)
}

func main() {
	yearTotal := 30
	a0 := 1000000.0
	n := yearTotal * 12
	r := 0.025 / 12.0

	principal := a0 * compound(float64(n), r)
	sumPrincipal := principal

	for year := yearTotal; year > 0; year-- {
		for month := 12; month > 0; month-- {
			if year == yearTotal && month == 12 {
			} else {
				principal /= (1 + r)
				sumPrincipal += principal
			}
			interest := sumPrincipal * r
			fmt.Printf("yy=%d, mm=%d, total=%.2f (principal=%.2f + interest=%.2f)\n", year, month, principal+interest, principal, interest)
		}
	}
}
