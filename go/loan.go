/*
final month: a0*r + a0 == C

(a0+a1) * r + a1 == C
  ==>  (a0+a1) * r + a1 == a0*r + a0
  ==>  a1*r + a1 == a0 == a1 * (r+1)


(a0+a1+a2) * r + a2 == C
  ==>  (a0+a1+a2) * r + a2 == (a0+a1) * r + a1
  ==>  a2 * (r+1) == a1


b == 1/(r+1)

1 + b^1 + b^2 + ... + b^(n-1) == S
  ==>
    b^1 + b^2 + ... + b^(n-1) + b^n == S*b
  ==>  1 - b^n == (1-b)*S
  ==>  S == (b^n - 1) / (b-1)
*/

package main

import (
	"fmt"
	"math"
)

func geometricSum(n, r float64) float64 {
	b := 1.0 / (r + 1.0)
	return (b - 1) / (math.Pow(b, n) - 1.0)
}

func amortization(yearTotal int, principalTotal, r float64) {
	principal := principalTotal * geometricSum(float64(yearTotal*30), r)
	sumPrincipal := 0.0

	for year := yearTotal; year > 0; year-- {
		for month := 12; month > 0; month-- {
			if year != yearTotal || month != 12 {
				// no need for the last month
				principal /= (1 + r)
			}
			sumPrincipal += principal
			interest := sumPrincipal * r
			fmt.Printf("yy=%d, mm=%d, total=%.2f (principal=%.2f + interest=%.2f)\n", year, month, principal+interest, principal, interest)
		}
	}
}

func main() {
	yearTotal := 30
	principalTotal := 1000000.0
	rateMonthly := 0.03 / 12.0

	amortization(yearTotal, principalTotal, rateMonthly)
}
