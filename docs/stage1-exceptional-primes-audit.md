# First-stage exceptional primes at modulus 24

The pinned `QH.stage1` theorem chooses a single positive constant before all stage parameters. Its proof bounds two bad sets, one for failure of a zero-free box and one for a weighted sum exceeding a cutoff somewhere on an interval. This audit checks the source statements and proof applications. The finite character and prime computations and the standalone Lean proof of primitive reduction supply independent checks of their respective steps. The analytic exceptional-prime estimate remains an upstream theorem under review. [Pinned mirror import][commit] · [Raw hashes and declaration spans](../data/stage1-sources.json) · [Run report](codex-task-05-result.md)

## Statement and specialization

The binders in `Stage1Succ.lean` 36–39, in order, are

$$
\exists C>0,\quad
\forall \varepsilon,\tau,K,\eta\in\mathbb R,\ \forall N_0\in\mathbb N,\quad
\left(0<\varepsilon<1/52,\ 0<\tau,\ 1\le K,\ 0<\eta,\ 0<N_0\right)
\Rightarrow \exists Y_0\in\mathbb R,\ \forall Y\ge Y_0.
$$

For each such $Y$ the conclusion gives a nonempty $\texttt{primePairSetFirst}(Y^{\varepsilon/5})$ and quantifies over **every** finite subset $B$ of that set. If every $q\in B$ fails `GoodQ` at the displayed parameters, its cardinality is at most $\eta$ times the candidate cardinality. There is no premise $\eta<1$, relation between $\tau$ and $\varepsilon$, or arithmetic restriction on $N_0$ beyond positivity. [Statement and proof][stage1]

With $(\varepsilon,\tau,K,\eta,N_0)=(1/100,1/200,2,1/4,24)$, set $z=Y^{1/500}$, $U=e^z$, and $P_Y=\texttt{PPset}\ 8\ 3\ U$. The inequalities on the parameters hold, including $1/100<1/52$. The **same** $C>0$ chosen before arbitrary parameters in the source gives a $Y_0$ for these values such that, for all $Y\ge Y_0$,

$$
P_Y\ne\varnothing,\qquad
\forall B\subseteq P_Y,\quad
\bigl(\forall q\in B,\ \neg\texttt{GoodQ}\ 24\ C\ (1/200)\ Y\ (Y^2)\ z\ q\bigr)
\ \Longrightarrow\ |B|\le |P_Y|/4 .
$$

The source defines `PPset` by filtering $1\le q\le\lfloor U\rfloor_+$ for primality, $q\bmod m_0=a_0\bmod m_0$, and $U^{1/2}<q$. For positive $U$ this is precisely the prime window $\sqrt U<q\le U$ with the stated residue. The upper edge is inclusive and the lower edge is strict. [First candidate set][defs] · [Filter][ppset]

## What a prime must satisfy

`GoodQ` says that for **every** complex Dirichlet character $\xi$ at level $N_0$, `BoxAll` holds for $Q=N_0 e^z$, $X=Y^K$, $M=N_0q$, and $n\mapsto\xi(n)J_q(n)$, where $J_q(n)$ is the Jacobi symbol. `BoxAll` in turn quantifies over **every** natural $N$ with `NeZero N` and every character $\psi$ at that level. Its antecedent `Ind` asks for primitivity and agreement on all $n$ coprime to $M$. There is no separate $N\mid M$ premise. In the general `stage` proof the arbitrary $M$ in the badness witness need only be nonzero. In the application to `stage1` it is $N_0q$. [Definitions][defs] · [General badness predicate][stage]

For each such inducer the conclusion `Box` requires all of the following.

- `GoodC` requires $\psi\ne 1$, $N\le Q$, and `ZeroFreeBox`. The latter requires $L(\psi,s)\ne0$ for every $s\in\mathbb C$ with $\Re s>1-1/400$ and $|\Im s|\le Q$. This uses a strict real boundary, an inclusive height boundary, and no upper bound on the real part. The height in the specialization is $24e^{Y^{1/500}}$. [GoodC][defs] · [ZeroFreeBox][zerofree]
- $|L'(\psi,1)/L(\psi,1)|\le C\log Y$, with the quotient defined from the derivative of the continued L-function. [Box][defs] · [Logarithmic derivative and weighted sums][weights]
- $|G_\psi(y)|\le y^{1/2+\tau}$ for **all real** $y\in[Y,Y^K]$, with
  $$
  G_\psi(y)=\sum_{1\le n\le y}\Lambda(n)\psi(n)(y/n-1)
             +yL'(\psi,1)/L(\psi,1).
  $$
  [Box][defs] · [Weighted sum][weights]

The restriction $\psi\ne1$ is essential to the logarithmic derivative estimate at $1$, since the principal L-function has a pole there. The original $\xi$ may be principal. The proof obtains a **nonprincipal primitive twist** by an odd prime disjoint from the inducing conductor. It does not test $G_\xi$ for the untwisted principal character. [Twist construction][twist-prim] · [Different normalization for the principal case][weights]

## How the source bounds the exceptional fraction

`QH.stage` starts with $\exists C>0$ followed by arbitrary $\varepsilon,\tau,K,\eta\in\mathbb R$ and $R\in\mathbb N$, with $0<\varepsilon\le1/4$, $0<\tau$, $1\le K$, and $0<\eta$. It then chooses $Y_0$ before $Y\ge Y_0$ and before $U,F,m_0,a_0,\Xi$. Here $\Xi$ is a finite set of primitive characters packaged with their positive levels, with levels at most $F$, $|\Xi|\le R$, and $1\le F\le\sqrt U$. The `admitted` Prop record requires $m_0>0$, $8\mid m_0$, $(a_0,m_0)=1$, and

$$
\tfrac14(\log Y)^2\log m_0\le\log U,\qquad
Y^{\varepsilon/6}\le\log U\le Y^{\varepsilon/5}(\log Y)^2.
$$

A separate premise requires every prime $p\mid m_0$ to satisfy $p\le Y^{\varepsilon/5}$ or $p>(Y^K)^{400}$. `stage1` constructs these inputs using $F=N_0$, $m_0=8,a_0=3,U=e^{Y^{\varepsilon/5}}$, and $\Xi$ the image of all $N_0$-characters under primitive reduction. It takes $R$ to be the cardinality before taking the image, which is 8 at level 24. The additional eventual bounds are $(\log Y)^2\le z/2$, $z\ge 2N_0$, $\log Y\ge1$, and $Y\ge1$. The first and $\log 8\le8$ give the `log_m` field. The second handles $2\mid8$ and gives $N_0\le e^{z/2}$ via $1+z/2\le e^{z/2}$. [Stage and admitted hypotheses][stage] · [Record][defs] · [Application][stage1]

Put $Q=FU$, $X=Y^K$, $Z=X^{400}$, $P=\texttt{PPset}\ m_0\ a_0\ U$. The proof chooses $Y$ large enough that $U\ge4$ and $(3/2)Y^{\varepsilon/5}(\log Y)^2\le Y^{\varepsilon/4}$. The latter is equivalent on the positive range to $(3/2)(\log Y)^2\le Y^{\varepsilon/20}$. The admitted bounds and $0\le\log F\le(\log U)/2$ put $\log Q$ in $[Y^{\varepsilon/6},Y^{\varepsilon/4}]$. The proof takes the maximum of the thresholds for `box_of_S`, `meanSqK`, `bad_share`, `count_a`, and these scale inequalities. Thus every use of $C$ and $Y_0$ is upstream of $Y$, including the choices made to bound the bad sets. [Thresholds and log range][stage]

### Boxes, primitive twists, and the zero-density loss

The filter $B_1\subseteq B$ collects primes for which some primitive character at level $fq$, with $f\le F$ and $fq\le Q$, fails `ZeroFreeBox`. For each $\xi\in\Xi$, $B_2(\xi)\subseteq B$ collects primes for which some $y\in[Y,X]$ has $|S(Z,y,q,\xi)|>y^{1/2+\tau}/2$. For a prime of $B$ outside the union of these filters, $q>\sqrt U\ge F$ and $U\ge4$ give an odd prime coprime to the level $f\le F$ of the relevant $\xi$. `twist_prim` produces a nonprincipal primitive character at $fq$ agreeing with $\xi(n)J_q(n)$ on every $n$. The level is $\le Q$, exclusion from $B_1$ gives the box, and exclusion from $B_2(\xi)$ gives the small-sum premise. `ind_unique` identifies any competing primitive inducer for $M\ne0$ with this one. Its proof changes both characters to a common level $NN'M$, then uses factorization through $\gcd(N,N')$ and primitivity. This proves the source inclusion $B\subseteq B_1\cup\bigcup_{\xi\in\Xi}B_2(\xi)$. [Filters and inclusion][stage-union] · [Primitive twist][twist-prim] · [Inducer uniqueness][ind-unique]

`box_of_S` takes $C$ from `kappaC`, used for the logarithmic derivative bound on the stated $\log Q$ range under `GoodC`. It takes a separate threshold from `tailK`, used to bound $|X\,\texttt{tailL}(\psi,Z)|\le Y^\varepsilon$. Both calls are applied to a **given** zero-free box through `GoodC`. Finite splitting gives $G_\psi(y)=-S(Z,y,q,\xi)-y\,\texttt{tailL}(\psi,Z)$, with $\texttt{tailL}=-L'/L(\psi,1)-\sum_{n\le Z}\Lambda(n)\psi(n)/n$. This splitting also follows algebraically by splitting the finite sum at $y$. As $y\le X$, the tail contribution is at most $Y^\varepsilon\le y^{1/2+\tau}/2$ for $Y\ge16,\varepsilon\le1/4,\tau>0$. These bounds give `Box`. The statements about `kappaC` and `tailK` here describe the visible applications, with their proofs beyond the selection. [Box producer][box] · [Weights][weights] · [Finite-splitting type][split] · [Named witness][split-proof]

`count_bad` calls `count_bad_core`, which injects $q\in B_1$ into a finite set of primitive characters paired with their levels. If $fq=f'q'$ and $q\ne q'$, primality would give $q\mid f'$, impossible since $f'\le F<q$. Failure of a box supplies an actual zero in the specified region. The source applies `zero_density_box` to count the pairs at levels $\le Q$ for $Q\ge3$, yielding $C_bQ^{1/4}$. The named density producer assembles coefficient-square, mollifier, zero-detection, duality, pair-twist and numerical estimates. Its assembly code is visible and those estimates remain deeper checks. With $F\le\sqrt U$, the proof uses

$$
|B_1|\le C_b(FU)^{1/4}\le |C_b|U^{3/8}\le(\eta/2)U^{9/10}\le(\eta/2)|P|.
$$

The penultimate inequality holds eventually since $9/10-3/8=21/40$. `stage_pow` chooses $U_0$ using $U^{21/40}\ge2|C_b|/\eta$ and $U\ge4$. The lower bound on $\log U$ and $\log U\le U-1$ let the proof enforce $U\ge U_0$ through a threshold in $Y$. [Count][count-bad] · [Injection][count-core] · [Density producer][density] · [Exponent comparison][stage-loss]

### The mean square and the move from fixed to varying points

The exact `MeanSq` premise controls $\sum_{q\in P}|S(Z,y,q,\kappa)|^2\le C_m y\log y\,|P|$ for **each** $y\in[Y,X]$ and **every** sequence $\kappa$ with $|\kappa(n)|\le1$, where $S(Z,y,q,\kappa)=\sum_{n\le Z}\Lambda(n)\min(1,y/n)\kappa(n)J_q(n)$. There is no multiplicativity premise. The nearby proposition `MeanSquareHypW` includes multiplicativity, an $a_0\bmod 4$ restriction, and its own count lower bound. `stage` uses `meanSqK` with `MeanSq`. [Definitions][defs] · [Other mean-square proposition][pnt-type] · [Actual mean-square theorem][mean-sq]

`meanSqK` chooses $C_m>0$ before $\varepsilon,K,Y$ from four constants for the prime-power coefficient bounds. It uses `meanSq_abs` with the correlation estimate `twistK` at $A=800K,\ B=K+1$. The eventual inequalities $1600K\log Y\le Y^{\varepsilon/6}$ and $400K\log Y\le\sqrt Y$ let it ensure $q>\lfloor Z\rfloor^2$ and absorb the coefficient sum in the error. Specifically $Z^2=Y^{800K}\le\sqrt U$, the stated coefficient bound is $\sum_{n\le Z}c_N(y,n)\le C_4y\log Z$, and $Y^{-(K+1)}(C_4y\log Z)^2\le C_4^2 y$ for $Y\le y\le Y^K$. The code separately controls the squared prime-power sums and the remainder from even exponents or primes dividing $m_0$. [Mean-square assembly][mean-sq] · [Prime-power groupings][pnt-type]

`twistK` chooses an exceptional index $n_*$ after $Y,U,m_0,a_0$, then controls every odd squarefree $1<s\le Y^A$ coprime to $m_0$ with $s\ne n_*$:

$$
\left|\sum_{q\in P} (q/s)\right|\le Y^{-B}|P|.
$$

The proof uses relative PNT in progressions with modulus $m_0s$, `count_a`, and `page_across` applied to `zFRDirichlet`. The at-most-one exceptional index comes from comparing sufficiently near-one real zeros across these moduli and separating the Jacobi characters on unit classes. In the mean-square calculation this controls off-diagonal correlations after reciprocity and squarefree reduction. The latter description is the mathematical reading of the `meanSq_abs` call and its arguments. The proof body of `meanSq_abs` is outside the selection. [Correlation statement and analytic inputs][twist-k] · [Exceptional-index uniqueness][twist-k-unique] · [Call][mean-sq]

Applying a pointwise mean square at a witness $y_q$ that changes with $q$ would be invalid. `bad_share` uses a block argument. For $T\le W\le2T$, write $D_q(v)$ for the right derivative of $S(Z,v,q,\kappa)$, obtained by retaining terms with $n>v$ and using $\Lambda(n)/n$ as the weight. The identity $vD_q(v)=S(Z,v,q,\kappa\,1_{n>v})$ gives $\sum_q |D_q(v)|^2\le C_m\log v\,|P|/v$ for $v>0$. This is where the quantification over all bounded sequences is needed. Integrating the derivative and using Cauchy–Schwarz gives, for arbitrary $w_q\in[T,W]$,

$$
\sum_{q\in P}|S(Z,w_q,q,\kappa)|^2
\le 2\sum_{q\in P}|S(Z,T,q,\kappa)|^2+
     2T\int_T^W\sum_{q\in P}|D_q(v)|^2\,dv
\le 4 C_m T\log(2T)\,|P|.
$$

Markov's inequality divides by $T^{1+2\tau}/4$. With $T\ge2$ and $\log(2T)\le2T^\tau/\tau$, the bad fraction on the block is at most $32C_m T^{-\tau}/\tau$. For $T=2^iY$ the dyadic blocks give an upper bound $32C_m Y^{-\tau}/[\tau(1-2^{-\tau})]$. The proof uses a threshold making this at most $\eta/(2(R+1))$. At $R=8,\eta=1/4$, this is $1/72$ per seed. The finite union uses $|\Xi|\le R\le R+1$ to get at most $(\eta/2)|P|$, then adds the other half from $B_1$. [Derivative and integral identities][bad-deriv] · [Block, Markov and geometric sum][bad-share] · [Union][stage-loss]

### Positive supply of candidate primes

`count_a` is conditional on two propositions, `PNTAPRelW` and `ExcBound`. `stage` passes actual named theorem terms for both. In `PNTAPRelW` the constants $c_3>0,A_0,C_0$ come before the positive modulus $M$ divisible by 8. The optional exceptional pair $e$ comes after that modulus and before the count cutoff $U$ and reduced class $a$. For $U\ge2$ and $\log U\ge C_0\log M\log(\log M+2)$ the relative error about the main term is bounded by

$$
A_0\bigl(e^{-c_3\log U/\log M}+e^{-\sqrt{c_3\log U}}\bigr).
$$

The main term is $\operatorname{li}(U)/\varphi(M)$ when $e$ is absent. When $e=(\chi_1,\beta_1)$, it is $(\operatorname{li}(U)-\Re\chi_1(a)\operatorname{li}(U^{\beta_1}))/\varphi(M)$. The selected zero has $1-1/(8\log M)<\beta_1<1$ and the character is nonprincipal with $\chi_1^2=1$. The PNT producer combines near and far ranges for a Chebyshev count, using explicit formulas, zero density and a Deuring–Heilbronn estimate for the far range. [PNT statement and main term][pnt-type] · [PNT producer][pnt]

`count_a` uses `ExcBound` at exponent $1$, giving a constant $c_0>0$ before the modulus and the nonprincipal real-character zero under consideration. It sets $c=\min(c_0,1)$ and uses $\beta_1\le1-c/M$. The source term for `excBound` supplies `siegelLower` to `excBound_of_siegelLower`, which calls `exceptional_zero_bound_of` with that input and `lfunction_deriv_near_one`. The exponent-$1$ bound is read from the use in `count_a`. The distinction between the conditional producer and its supplied term matters for the dependency audit. [Exceptional bound producer][exc] · [Use at exponent 1][count-a]

The implementation makes the relative error at most $1/2$. Even with a subtractive exceptional term, $\log U\ge4$ and $1-\beta_1\ge c/M$ give $U-U^{\beta_1}\ge cU/(2M)$. Integrating $1/\log t$ and using $\varphi(M)\le M$ gives a main term at least $cU/(2M^2\log U)$. The admissible range for large $Y$ gives $\log U\ge80\log M$, $\log(320/c)\le(\log U)/20$, and the PNT cutoff condition. The first two inequalities imply $cU/(2M^2\log U)\ge 4U^{9/10}$. The AP count is at least half the main term, and subtracting the at most $\sqrt U$ primes at or below the lower edge leaves $|P|\ge U^{9/10}>0$. The source takes the threshold in $Y$ before $U,M,a$ using the admitted bounds and the PNT and exceptional-zero constants. [Main-term lower bound and sizing][main-ap] · [Error and range transfer][count-pos] · [Threshold][count-a]

## Scope and failure modes

`admitted` stores arithmetic and size hypotheses in a Prop record. `GoodC` and `MeanSq` are propositions supplied conditionally to some lemmas. Likewise `PNTAPRelW` and `ExcBound` are hypotheses of `count_a`, with theorem applications discharging them in `stage`. The visible proof terms also construct `meanSqK` and `count_bad` from analytic estimates. These are source-level facts about proof wiring and hypotheses. The selected declarations show no explicit input equivalent to all-character Dirichlet GRH and no explicit appeal to the headline GRH theorem. The box restricts both the region and the family, and the count permits exceptions. The imported analytic proofs beyond the pinned bodies and the transitive upstream axiom set remain unaudited here. [Immediate inputs][stage] · [Density producer][density] · [PNT producer][pnt] · [Exceptional bound producer][exc]

Moving $C$ after $Y$ would allow the logarithmic derivative bound to rescale at each test point. Allowing $Y_0$ to vary with $Y$ would lose the eventual assertion. Reasoning from a pointwise mean square directly at different $y_q$ would lose uniformity. Using the untwisted principal character at $1$ would mishandle the pole, and dropping conductor coprimality could let a twist cancel a local character factor. An empty candidate set makes the bad-set inequality vacuous. These are distinct conditions checked at different stages of the source argument. [Constant order and nonemptiness][stage] · [Uniformity step][bad-share] · [Twist hypotheses][twist-prim]

## Independently checked finite diagnostics

On $(\mathbb Z/24\mathbb Z)^\times$, the mod-3 basis character is $+1$ at 1 and $-1$ at 2, the mod-4 basis is $+1$ at 1 and $-1$ at 3, and the mod-8 basis is $+1$ at 1 and 7 and $-1$ at 3 and 5. Each depends on the residue at its named modulus and is extended by zero on nonunits at level 24. The mod-4 and mod-8 signs distinguish all four units modulo 8. Together with the mod-3 sign, the Chinese remainder theorem makes the sign triple a bijective group homomorphism onto $\{\pm1\}^3$. All characters are therefore the eight products with exponent triples in $\{0,1\}^3$.

To compute the conductor at level $L$, the script enumerates divisors $d\mid L$ in increasing order and checks equality of values on every fibre of unit reduction modulo $d$. Unit reduction is onto by lifting at each prime power and using the Chinese remainder theorem. Fibre equality is therefore equivalent to factorization through the unit group at $d$. The first passing divisor is the conductor. Twists multiply the level-24 values by Legendre symbols at $q$, computed by listing nonzero squares. The tests independently compare them with Euler's criterion and also check unit-fibre agreement and primitivity of the resulting tables. [Diagnostic code](../tools/mod24_prime_diagnostics.py) · [Tests](../tests/test_mod24_prime_diagnostics.py)

| Exponents (mod 3, 4, 8) | $f$ | Conductor at $q=11$ | Conductor at $q=19$ |
| --- | ---: | ---: | ---: |
| $0,0,0$ | 1 | 11 | 19 |
| $0,0,1$ | 8 | 88 | 152 |
| $0,1,0$ | 4 | 44 | 76 |
| $0,1,1$ | 8 | 88 | 152 |
| $1,0,0$ | 3 | 33 | 57 |
| $1,0,1$ | 24 | 264 | 456 |
| $1,1,0$ | 12 | 132 | 228 |
| $1,1,1$ | 24 | 264 | 456 |

The computed base multiset is $1,3,4,8,8,12,24,24$. Both twists give conductor $fq$ in every row. At level $M=24q$, the primitive character $\psi$ of level $fq$ satisfies $\psi(n)=\xi(n)J_q(n)$ on $(n,M)=1$, the exact agreement needed by `Ind`. For example, at $q=11$ with $\xi$ principal modulo 24, $\psi(2)=-1$ while the product at level $264$ vanishes at $2$. The product at level $24q$ is primitive only in the rows with $f=24$. If one allows $q=3$, the mod-3 basis character multiplied by $J_3$ is trivial on all units at level 72, illustrating the loss of the $fq$ rule when the conductor and prime share a factor.

The prime windows use a rational enclosure of $e^z$. For $0\le z\le4$, summing through $z^{16}/16!$ gives a lower bound. The remainder is at most $(z^{17}/17!)/(1-z/18)$ since every subsequent term ratio is at most $z/18$. The endpoints give the same floor at $z=3$ and at $z=4$. For $U\ge0$, $\lfloor\sqrt U\rfloor=\operatorname{isqrt}(\lfloor U\rfloor)$, so the strict edge can be evaluated in integers.

| $z$ | $\lfloor e^z\rfloor$ | $\lfloor\sqrt{e^z}\rfloor$ | $P$ | $\lfloor\lvert P\rvert/4\rfloor$ |
| ---: | ---: | ---: | --- | ---: |
| 3 | 20 | 4 | $11,19$ | 0 |
| 4 | 54 | 7 | $11,19,43$ | 0 |

If the eventual estimate were applicable at $Y=3^{500}$, its bound would force every bad subset of the two candidates to be empty. The source gives no such threshold guarantee. Its sufficient conditions use $z\ge48$ for level 24. In fact the `log_m` inequality here would require $(\log Y)^2\log 8/4\le z$, which fails at $Y=z^{500}$ for $z=3,4$. The sample calculations check primality, the window, conductors, and unit agreement. They supply no information about `GoodQ` or zeros of L-functions. [Source thresholds][stage1] · [Exact implementation](../tools/mod24_prime_diagnostics.py)

[commit]: https://github.com/CocoSgt/riemann-hypothesis-lean/commit/0fb9869c6e6d7b54b67de803af0e0be29d37fc22
[stage1]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/Stage1Succ.lean#L36-L96
[stage]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/StagePow.lean#L41-L99
[stage-union]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/StagePow.lean#L100-L139
[stage-loss]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/StagePow.lean#L141-L170
[defs]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/PrimeSetTwoBounds.lean#L13-L49
[ppset]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/SecondEstimateOfIntervalHypothesis.lean#L50-L51
[zerofree]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/SecondEstimateOfIntervalHypothesis.lean#L44-L45
[weights]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/SecondEstimateOfIntervalHypothesis.lean#L14-L29
[split]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/SecondEstimateOfIntervalHypothesis.lean#L119-L121
[split-proof]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/ZeroFreeRegionGl2PrimeChoiceResults.lean#L49-L54
[twist-prim]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/TwistPrim.lean#L9-L18
[ind-unique]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/IndUnique.lean#L7-L51
[box]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/BoxOfS.lean#L28-L60
[count-bad]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/CountBad.lean#L9-L16
[count-core]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/CountBadCore.lean#L8-L53
[density]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/JacobiCharacterSums/CountZAll.lean#L13-L15
[mean-sq]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/meanSqK.lean#L51-L221
[twist-k]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/twistK.lean#L148-L159
[twist-k-unique]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/twistK.lean#L249-L282
[pnt-type]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/JacobiCharacterSums/MeanSquareHypWIff.lean#L13-L55
[bad-deriv]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/BadShare.lean#L62-L96
[bad-share]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Development/AutomorphicArithmetic/MeanSquareBounds/BadShare.lean#L118-L318
[count-a]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/JacobiCharacterSums/MSqCount.lean#L346-L386
[main-ap]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/JacobiCharacterSums/MSqCount.lean#L86-L203
[count-pos]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/JacobiCharacterSums/MSqCount.lean#L205-L344
[pnt]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/GL3MeanSquares/GenusMeanAsymptotics/JacobiCharacterSums/PNTFinal.lean#L16-L24
[exc]: https://github.com/CocoSgt/riemann-hypothesis-lean/blob/0fb9869c6e6d7b54b67de803af0e0be29d37fc22/src/Formalism/LandauZeroFreeBounds/SiegelWalfiszAPOfSiegelLower.lean#L26-L32
