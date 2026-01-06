<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 15/15 -->

  - We use indexed parentheses – such as (x) _𝑖_, (X) _𝑖𝑗_, or (X) _𝑖_ 1 _...𝑖𝑛_   - to denote elements of vectors,
matrices, and tensors, respectively. If a vector x ∈ R _[𝑎]_ is used in a context that requires a
matrix, the vector is interpreted as an ( _𝑎,_ 1)-matrix (i.e., a column vector) and can be turned
into a row vector (i.e., a (1 _,𝑎_ )-matrix) using the transpose operation x _[𝑇]_ . We use x [D] ∈ R _[𝑎,𝑎]_ to


128


Table 8. Details for selected knowledge graph embeddings, including the plausibility scoring function
_𝜙_ ( _𝜀_ ( _𝑠_ ) _, 𝜌_ ( _𝑝_ ) _,𝜀_ ( _𝑜_ )) for edge _[𝑠]_ _𝑝_ _𝑜_, and other conditions applied


**Model** _𝜙_ ( _𝜀_ ( _𝑠_ ) _, 𝜌_ ( _𝑝_ ) _,𝜀_ ( _𝑜_ )) **Conditions** (for all _𝑥_ ∈ _𝑉_, _𝑦_ ∈ _𝐿_ )


TransE [63] −∥e _𝑠_ + r _𝑝_ - e _𝑜_ ∥ _𝑞_ e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, _𝑞_ ∈{1 _,_ 2}, ∥e _𝑥_ ∥2 = 1


e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, w _𝑦_ ∈ R _[𝑑]_,
TransH [553] −∥(e _𝑠_ −(e _𝑠_ [T] w _𝑝_ )w _𝑝_ ) + r _𝑝_ −(e _𝑜_ −(e _𝑜_ [T] w _𝑝_ )w _𝑝_ ) ∥ [2] 2 ∥w _𝑦_ ∥2 = 1, w∥r [T] _𝑦𝑦_ r∥ _𝑦_ 2 [≈] [0,][ ∥][e] _[𝑥]_ [∥][2][ ≤] [1]


e _𝑥_ ∈ R _[𝑑][𝑒]_, r _𝑦_ ∈ R _[𝑑][𝑟]_, W _𝑦_ ∈ R _[𝑑][𝑟]_ _[,𝑑][𝑒]_,
TransR [271] −∥W _𝑝_ e _𝑠_ + r _𝑝_ - W _𝑝_ e _𝑜_ ∥ [2] 2 ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1, ∥W _𝑦_ e _𝑥_ ∥2 ≤ 1


e _𝑥_ ∈ R _[𝑑][𝑒]_, r _𝑦_ ∈ R _[𝑑][𝑟]_, w _𝑥_ ∈ R _[𝑑][𝑒]_, w _𝑦_ ∈ R _[𝑑][𝑟]_,
TransD [271] −∥(w _𝑝_ ⊗ w _𝑠_ + I)e _𝑠_ + r _𝑝_ −(w _𝑝_ ⊗ w _𝑜_ + I)e _𝑜_ ∥ [2] 2 ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1, ∥(w _𝑦_ ⊗ w _𝑥_ + I)e _𝑥_ ∥2 ≤ 1


RotatE [511] −∥e _𝑠_ ⊙ r _𝑝_ - e _𝑜_ ∥2 e _𝑥_ ∈ C _[𝑑]_, r _𝑦_ ∈ C _[𝑑]_, ∥r _𝑦_ ∥2 = 1


RESCAL [386] e _𝑠_ [T] R _𝑝_ e _𝑜_ e _𝑥_ ∈ R _[𝑑]_, R _𝑦_ ∈ R _[𝑑,𝑑]_, ∥e _𝑥_ ∥2 ≤ 1, ∥R _𝑦_ ∥2 _,_ 2 ≤ 1


DistMult [568] e _𝑠_ [T] r _𝑝_ [D] e _𝑜_ e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, ∥e _𝑥_ ∥2 = 1, ∥r _𝑦_ ∥2 ≤ 1


HolE [385] r _𝑝_ [T] (e _𝑠_ _★_ e _𝑜_ ) e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1


ComplEx [526] Re(e _𝑠_ [T] r _𝑝_ [D] ~~e~~ _𝑜_ ) e _𝑥_ ∈ C _[𝑑]_, r _𝑦_ ∈ C _[𝑑]_, ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1


SimplE [283] e _𝑠_ [T] r _𝑝_ [D] w _𝑜_ +e _𝑜_ [T] w _𝑝_ [D] w _𝑠_ e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, w _𝑥_ ∈ R _[𝑑]_, w _𝑦_ ∈ R _[𝑑]_,

2 ∥e _𝑥_ ∥2 ≤ 1, ∥w _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1 _,_ ∥w _𝑦_ ∥2 ≤ 1


TuckER [30] W ⊗1 e _𝑠_ [T] ⊗2 r _𝑝_ [T] ⊗3 e _𝑜_ [T] e _𝑥_ ∈ R _[𝑑][𝑒]_, r _𝑦_ ∈ R _[𝑑][𝑟]_, W ∈ R _[𝑑][𝑒]_ _[,𝑑][𝑟]_ _[,𝑑][𝑒]_


SME Linear [192] (Ve _𝑠_ + V [′] r _𝑝_ + v) [T] (We _𝑜_ + W [′] r _𝑝_ + w) e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, v ∈ R _[𝑤]_, w ∈ R _[𝑤]_, ∥e _𝑥_ ∥2 = 1,
V ∈ R _[𝑤,𝑑]_ _,_ V [′] ∈ R _[𝑤,𝑑]_ _,_ W ∈ R _[𝑤,𝑑]_ _,_ W [′] ∈ R _[𝑤,𝑑]_

SME Bilinear [192] ((V ⊗3 r _𝑝_ [T] )e _𝑠_ + v) [T] ((W ⊗3 r _𝑝_ [T] )e _𝑜_ + w) eV ∈ _𝑥_ ∈ RR _[𝑑][𝑤,𝑑,𝑑]_, r _𝑦_, W ∈∈ R _[𝑑]_, vR ∈ _[𝑤,𝑑,𝑑]_ R _[𝑤]_, w ∈ R _[𝑤]_, ∥e _𝑥_ ∥2 = 1,




               - �e _𝑠_
NTN [488] r _𝑝_ [T] _𝜓_ e _𝑠_ [T] We _𝑜_ + W
e _𝑜_




- - e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, w ∈ R _[𝑤]_, W ∈ R _[𝑤,]_ [2] _[𝑑]_,
+ w W ∈ R _[𝑑,𝑤,𝑑]_, ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1,
∥w ∥2 ≤ 1, ∥W ∥2 _,_ 2 ≤ 1, ∥W1 [[·] ≤ [:] _𝑖_ _[𝑖]_ [:] ≤ [·]] _𝑤_ [∥][2] _[,]_ [2][ ≤] [1]


e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, v ∈ R _[𝑤]_, w ∈ R _[𝑤]_, W ∈ R _[𝑤,]_ [3] _[𝑑]_

∥e _𝑥_ ∥2 ≤ 1 ∥r _𝑦_ ∥2 ≤ 1



e _𝑠_

MLP [131] v [T] _𝜓_ [�] W r _𝑝_

            -  

e _𝑜_

            -  



+ w [�]

  
  



 
W ∗




e _𝑠_ [[] _[𝑎,𝑏]_ []]
r _𝑝_ [[] _[𝑎,𝑏]_ []]



��� T
e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, _𝑑_ = _𝑎𝑏_,
W [�] e _𝑜_

    - W ∈ R _[𝑤]_ [1][ (] _[𝑤]_ [2][+][2] _[𝑎]_ [−][1][) (] _[𝑤]_ [3][+] _[𝑏]_ [−][1][)] _[,𝑑]_, W ∈ R _[𝑤]_ [1] _[,𝑤]_ [2] _[,𝑤]_ [3]

    


ConvE [127] _𝜓_ [�] vec

           
           





_𝜓_




             -              -              - T              - e _𝑥_ ∈ R _[𝑑][𝑒]_, r _𝑦_ ∈ R _[𝑑][𝑟]_, W ∈ R _[𝑤]_ [2][ (] _[𝑤]_ [1][+] _[𝑑][𝑒]_ [−][1][)] _[,𝑑][𝑒]_,
HypER [28] _𝜓_ vec r _𝑝_ [T] W ∗ e _𝑠_ W e _𝑜_ W ∈ R _[𝑑][𝑟]_ _[,𝑤]_ [1] _[,𝑤]_ [2]


denote the diagonal matrix with the values of the vector x ∈ R _[𝑎]_ on its diagonal. We denote
the identity matrix by I such that if _𝑗_ = _𝑘_, then (I) _𝑗𝑘_ = 1; otherwise (I) _𝑗𝑘_ = 0.








- We denote by







X1
_..._
Xn



the vertical stacking of matrices X1 _, . . .,_ X _𝑛_ with the same number of



columns. Given a vector x ∈ R _[𝑎𝑏]_, we denote by x [[] _[𝑎,𝑏]_ []] ∈ R _[𝑎,𝑏]_ the “reshaping” of x into an ( _𝑎,𝑏_ )matrix such that (x [[] _[𝑎,𝑏]_ []] ) _𝑖𝑗_ = (x) ( _𝑖_ + _𝑎_ ( _𝑗_ −1)) . Conversely, given a matrix X ∈ R _[𝑎,𝑏]_, we denote by



129


vec(X) ∈ R _[𝑎𝑏]_ the _vectorisation_ of X such that vec(X) _𝑘_ = (X) _𝑖𝑗_ where _𝑖_ = (( _𝑘_  - 1) mod _𝑚_ ) + 1
and _𝑗_ = _[𝑘]_ _𝑚_ [−] _[𝑖]_ [+][ 1 (observe that vec][(][x][[] _[𝑎,𝑏]_ []][)][ =][ x][).]

- Given a tensor X ∈ R _[𝑎,𝑏,𝑐]_, we denote by X [[] _[𝑖]_ [:][·][:][·]] ∈ R _[𝑏,𝑐]_, the _𝑖_ [th] _slice_ of tensor X along the first
mode; for example, given X ∈ R [5] _[,]_ [2] _[,]_ [3], then X [[][4:][·][:][·]] returns the (2 _,_ 3)-matrix consisting of the




      (X)411 (X)412 (X)413
elements
(X)421 (X)422 (X)423




. Analogously, we use X [[·][:] _[𝑖]_ [:][·]] ∈ R _[𝑎,𝑐]_ and X [[·][:][·][:] _[𝑖]_ []] ∈ R _[𝑏,𝑐]_ to



indicate the _𝑖_ [th] slice along the second and third modes of X, respectively.

- We denote by _𝜓_ (X) the element-wise application of a function _𝜓_ to the tensor X, such
that ( _𝜓_ (X)) _𝑖𝑛_ 1 _...𝑖𝑛_ = _𝜓_ (X _𝑖_ 1 _...𝑖𝑛_ ). Common choices for _𝜓_ include a sigmoid function (e.g., the
logistic function _𝜓_ ( _𝑥_ ) = 1+ _𝑒_ 1 ~~[−]~~ ~~_[𝑥]_~~ [or the hyperbolic tangent function] _[ 𝜓]_ [(] _[𝑥]_ [)][ =][ tanh] _[𝑥]_ [=] _[𝑒]_ _𝑒_ _[𝑥]_ ~~_[𝑥]_~~ [−] + _𝑒_ _[𝑒]_ ~~[−]~~ [−] ~~_[𝑥]_~~ _[𝑥]_ [),]

the rectifier ( _𝜓_ ( _𝑥_ ) = max(0 _,𝑥_ )), softplus ( _𝜓_ ( _𝑥_ ) = ln(1 + _𝑒_ _[𝑥]_ )), etc.



The first and most elemental operation we consider is that of matrix multiplication.


_Definition B.53 (Matrix multiplication)._ The _multiplication of matrices_ X ∈ R _[𝑎,𝑏]_ and Y ∈ R _[𝑏,𝑐]_ is
a matrix XY ∈ R _[𝑎,𝑐]_ such that (XY) _𝑖𝑗_ = [�] _[𝑏]_ _𝑘_ =1 [(][X][)] _[𝑖𝑘]_ [(][Y][)] _[𝑘𝑗]_ [. The matrix multiplication of two tensors]
X ∈ R _[𝑎]_ [1] _[,...,𝑎][𝑚][,𝑐]_ and Y ∈ R _[𝑐,𝑏]_ [1] _[,...,𝑏][𝑛]_ is a tensor XY ∈ R _[𝑎]_ [1] _[,...,𝑎][𝑚][,𝑏]_ [1] _[,...,𝑏][𝑛]_ such that (XY) _𝑖_ 1 _...𝑖𝑚𝑖𝑚_ +1 _...𝑖𝑚_ + _𝑛_ =

- _𝑐_
_𝑘_ =1 [(X)] _[𝑖]_ 1 _[...𝑖]_ _𝑚_ _[𝑘]_ [(Y)] _[𝑘𝑖]_ _𝑚_ +1 _[𝑖]_ _𝑚_ + _𝑛_ [.]


For convenience, we may implicitly add or remove modes with dimension 1 for the purposes of

matrix multiplication and other operators; for example, given two vectors x ∈ R _[𝑎]_ and y ∈ R _[𝑎]_, we
denote by x [T] y (aka the dot or inner product) the multiplication of matrix x [T] ∈ R [1] _[,𝑎]_ with y ∈ R _[𝑎,]_ [1]

such that x [T] y ∈ R [1] _[,]_ [1] (i.e., a scalar in R); conversely, xy [T] ∈ R _[𝑎,𝑎]_ (the outer product).


Constraints on embeddings are sometimes given in terms of norms, defined next.


_Definition B.54 (𝐿_ _[𝑝]_ _-norm, 𝐿_ _[𝑝,𝑞]_ _-norm)._ For _𝑝_ ∈ R, the _𝐿_ _[𝑝]_ _-norm_ of a vector x ∈ R _[𝑎]_ is the scalar

1
∥x∥ _𝑝_ ≔ (|(x)1| _[𝑝]_ + _. . ._ + |(x) _𝑎_ | _[𝑝]_ ) _𝑝_, where |(x) _𝑖_ | denotes the absolute value of the _𝑖_ [th] element of x.




_[𝑞]_ _𝑝_ - _𝑞_ [1]



For _𝑝,𝑞_ ∈ R, the _𝐿_ _[𝑝,𝑞]_ _-norm_ of a matrix X ∈ R _[𝑎,𝑏]_ is the scalar ∥X∥ _𝑝,𝑞_ ≔ �� _𝑏𝑗_ =1 �� _𝑖𝑎_ =1 [|(][X][)] _[𝑖𝑗]_ [|] _[𝑝]_ [�] _[𝑞]_ _𝑝_



_𝑞_
.



The _𝐿_ [1] norm (i.e., ∥x∥1) is thus simply the sum of the absolute values of x, while the _𝐿_ [2] norm
(i.e., ∥x∥2) is the (Euclidean) length of the vector. The Frobenius norm of the matrix X then equates


_𝑏_ _𝑎_ 2
to ∥X∥2 _,_ 2 = �� _𝑗_ =1 �� _𝑖_ =1 [|(][X][)] _[𝑖𝑗]_ [|][2][��] [1] ; i.e., the square root of the sum of the squares of all elements.


Another type of product used by embedding techniques is the Hadamard product, which multi
plies tensors of the same dimension and computes their product element-wise.


_Definition B.55 (Hadamard product)._ Given two tensors X ∈ R _[𝑎]_ [1] _[,...,𝑎][𝑛]_ and Y ∈ R _[𝑎]_ [1] _[,...,𝑎][𝑛]_, the
_Hadamard product_ X ⊙Y is defined as a tensor in R _[𝑎]_ [1] _[,...,𝑎][𝑛]_, with each element computed as
(X ⊙Y) _𝑖_ 1 _...𝑖𝑛_ ≔ (X) _𝑖_ 1 _...𝑖𝑛_ (Y) _𝑖_ 1 _...𝑖𝑛_ .


Other embedding techniques – namely RotatE [511] and ComplEx [526] – uses _complex space_

based on complex numbers. With a slight abuse of notation, the definitions of vectors, matrices

and tensors can be modified by replacing the set of real numbers R by the set of complex numbers

C, giving rise to complex vectors, complex matrices, and complex tensors. In this case, we denote

by Re(·) the real part of a complex number. Given a complex vector x ∈ C _[𝐼]_, we denote by ~~x~~ its

complex conjugate (swapping the sign of the imaginary part of each element). Complex analogues

of the aforementioned operators can then be defined by replacing the multiplication and addition

of real numbers with the analogous operators for complex numbers, where RotateE [511] uses the

complex Hadamard product, and ComplEx [526] uses complex matrix multiplication.


130


One embedding technique – MuRP [29] – uses hyperbolic space, specifically based on the Poincaré

ball. As this is the only embedding we cover that uses this space, and the formalisms are lengthy

(covering the Poincaré ball, Möbius addition, Möbius matrix–vector multiplication, logarithmic

maps, exponential maps, etc.), we rather refer the reader to the paper for further details [29].


As discussed in Section 5.2, tensor decompositions are an important concept for many embeddings,

and at the heart of such decompositions is the tensor product.


_Definition B.56 (Tensor product)._ Given two tensors X ∈ R _[𝑎]_ [1] _[,...,𝑎][𝑚]_ and Y ∈ R _[𝑏]_ [1] _[,...,𝑏][𝑛]_, the _tensor_
_product_ X ⊗Y is defined as a tensor in R _[𝑎]_ [1] _[,...,𝑎][𝑚][,𝑏]_ [1] _[,...,𝑏][𝑛]_, with each element computed as (X ⊗
Y) _𝑖_ 1 _...𝑖𝑚_ _𝑗_ 1 _...𝑗𝑛_ ≔ (X) _𝑖_ 1 _...𝑖𝑚_ (Y) _𝑗_ 1 _...𝑗𝑛_ . [44]


To illustrate the tensor product, assume that X ∈ R [2] _[,]_ [3] and Y ∈ R [3] _[,]_ [4] _[,]_ [5] . The result of X ⊗Y will
be a tensor in R [2] _[,]_ [3] _[,]_ [3] _[,]_ [4] _[,]_ [5] . Element (X ⊗Y)12345 will be computed by multiplying (X)12 and (Y)345.


An _𝑛_ -mode product is used by other embeddings to transform elements along a mode of a tensor.


_Definition B.57 (𝑛-mode product)._ For a positive integer _𝑛_, a tensor X ∈ R _[𝑎]_ [1] _[,...,𝑎][𝑛]_ [−][1] _[,𝑎][𝑛][,𝑎][𝑛]_ [+][1] _[,...,𝑎][𝑚]_ and
matrix Y ∈ R _[𝑏,𝑎][𝑛]_, the _𝑛-mode product_ of X and Y is the tensor X ⊗ _𝑛_ Y ∈ R _[𝑎]_ [1] _[,...,𝑎][𝑛]_ [−][1] _[,𝑏,𝑎][𝑛]_ [+][1] _[,...,𝑎][𝑚]_ such
that (X ⊗ _𝑛_ Y) _𝑖_ 1 _...𝑖𝑛_ −1 _𝑗𝑖𝑛_ +1 _...𝑖𝑚_ ≔ [�] _𝑘_ _[𝑎][𝑛]_ =1 [(X)] _[𝑖]_ [1] _[...𝑖][𝑛]_ [−][1] _[𝑘𝑖][𝑛]_ [+][1] _[...𝑖][𝑚]_ [(][Y][)] _[𝑗𝑘]_ [.]


To illustrate, let us assume that X ∈ R [2] _[,]_ [3] _[,]_ [4] and Y ∈ R [5] _[,]_ [3] . The result of X ⊗2 Y will be a tensor
in R [2] _[,]_ [5] _[,]_ [4], where, for example, (X ⊗2 Y)142 will be given as (X)112(Y)41 + (X)122 (Y)42 + (X)132 (Y)43.
Observe that if y ∈ R _[𝑎][𝑛]_ - i.e., if y is a (column) vector – then the _𝑛_ -mode tensor product X ⊗ _𝑛_ y [T]

“flattens” the _𝑛_ [th] mode of X to one dimension, effectively reducing the order of X by one.


One embedding technique – HolE [385] – uses a circular correlation operator.


_Definition B.58 (Circular correlation)._ The _circular correlation_ of vector x ∈ R _[𝑎]_ with y ∈ R _[𝑎]_ is the
vector x _★_ y ∈ R _[𝑎]_ such that (x _★_ y) _𝑘_ ≔ [�] _𝑖_ _[𝑎]_ =1 [(][x][)] _[𝑖]_ [(][y][)] [(((] _[𝑘]_ [+] _[𝑖]_ [−][2][)][ mod] _[𝑎]_ [)+][1][)] [.]


Each element of x _★_ y is the sum of _𝑎_ elements along a diagonal of the outer product x ⊗ y that
“wraps” if not the primary diagonal. Assuming _𝑎_ = 5, then (x _★_ y)1 = (x)1(y)1 +(x)2(y)2 +(x)3(y)3 +
(x)4(y)4+(x)5(y)5, or a case that wraps: (x _★_ y)4 = (x)1(y)4+(x)2(y)5+(x)3(y)1+(x)4(y)2+(x)5(y)3.


Finally, a couple of neural models that we include – namely ConvE [127] and HypER [28] – are

based on convolutional architectures using the convolution operator.


_Definition B.59 (Convolution)._ Given two matrices X ∈ R _[𝑎,𝑏]_ and Y ∈ R _[𝑒,𝑓]_, the _convolution_ of X
and Y is the matrix X ∗ Y ∈ R [(] _[𝑎]_ [+] _[𝑒]_ [−][1][)] _[,]_ [(] _[𝑏]_ [+] _[𝑓]_ [−][1][)] such that (X ∗ Y) _𝑖𝑗_ = [�] _𝑘_ _[𝑎]_ =1 - _𝑏𝑙_ =1 [(][X][)] _[𝑘𝑙]_ [(][Y][)] [(] _[𝑖]_ [+] _[𝑘]_ [−] _[𝑎]_ [) (] _[𝑗]_ [+] _[𝑙]_ [−] _[𝑏]_ [)] [.][45]

In cases where ( _𝑖_ + _𝑘_ - _𝑎_ ) _<_ 1, ( _𝑗_ + _𝑙_ - _𝑏_ ) _<_ 1, ( _𝑖_ + _𝑘_ - _𝑎_ ) _> 𝑒_ or ( _𝑗_ + _𝑙_ - _𝑏_ ) _> 𝑓_ (i.e., where
(Y) ( _𝑖_ + _𝑘_ - _𝑎_ ) ( _𝑗_ + _𝑙_ - _𝑏_ ) lies outside the bounds of Y), we say that (Y) ( _𝑖_ + _𝑘_ - _𝑎_ ) ( _𝑗_ + _𝑙_ - _𝑏_ ) = 0.


Intuitively speaking, the convolution operator overlays X in every possible way over Y such that
at least one pair of elements (X) _𝑖𝑗,_ (Y) _𝑙𝑘_ overlaps, summing the products of pairs of overlapping
elements to generate an element of the result. Elements of X extending beyond Y are ignored
(equivalently we can consider Y to be “zero-padded” outside its borders). To illustrate, given X ∈ R [3] _[,]_ [3]

and Y ∈ R [4] _[,]_ [5], then X ∗ Y ∈ R [6] _[,]_ [7], where, for example, (X ∗ Y)11 = (X)33 (Y)11 (with the bottom
right corner of X overlapping the top left corner of Y), while (X ∗ Y)34 = (X)11 (Y)12 + (X)12 (Y)13 +


44Please note that “⊗” is used here in an unrelated sense to its use in Definition B.34.
45We define the convolution operator per the convention for convolutional neural networks. Strictly speaking, the operator

should be called _cross-correlation_, where traditional convolution requires the matrix X to be initially “rotated” by 180°. Since
in our settings the matrix X is learnt, rather than given, the rotation is redundant.


131


(X)13 (Y)14 + (X)21 (Y)22 + (X)22 (Y)23 + (X)23 (Y)24 + (X)31 (Y)32 + (X)32 (Y)33 + (X)33(Y)34 (with
(X)22 – the centre of X – overlapping (Y)23). [46] In a convolution X ∗ Y, the matrix X is often called

the “kernel” (or “filter”). Often several kernels are used in order to apply multiple convolutions.

Given a tensor X ∈ R _[𝑐,𝑎,𝑏]_ (representing _𝑐_ ( _𝑎,𝑏_ )-kernels) and a matrix Y ∈ R _[𝑒,𝑓]_, we denote by
X ∗ Y ∈ R _[𝑐,]_ [(] _[𝑎]_ [+] _[𝑒]_ [−][1][)] _[,]_ [(] _[𝑏]_ [+] _[𝑓]_ [−][1][)] the result of the convolutions of the _𝑐_ first-mode slices of X over Y such
that (X ∗ Y) [[] _[𝑖]_ [:][·][:][·]] = X [[] _[𝑖]_ [:][·][:][·]] ∗ Y for 1 ≤ _𝑖_ ≤ _𝑐_, yielding a tensor of results for _𝑐_ convolutions.


_B.6.3_ _Graph neural networks._ We now provide high-level definitions for graph neural networks

(GNNs) inspired by (for example) the definitions provided by Xu et al. [565]. We assume that the

GNN accepts a directed vector-labelled graph as input (see Definition B.46).


We first abstractly define a recursive graph neural network.


_Definition B.60 (Recursive graph neural network)._ A _recursive graph neural network_ ( _RecGNN_ ) is a

pair of functions ℜ≔ (Agg _,_ Out), such that (with _𝑎,𝑏,𝑐_ ∈ N):


  - Agg : R _[𝑎]_ × 2 [(][R] _[𝑎]_ [×][R] _[𝑏]_ [)→][N] → R _[𝑎]_

  - Out : R _[𝑎]_ → R _[𝑐]_


The function Agg computes a new feature vector for a node, given its previous feature vector and

the feature vectors of the nodes and edges forming its neighbourhood; the function Out transforms

the final feature vector computed by Agg for a node to the output vector for that node. We assume

that _𝑎_ and _𝑏_ correspond to the dimensions of the input node and edge vectors, respectively, while

_𝑐_ denotes the dimension of the output vector for each node. Given a RecGNN ℜ= (Agg _,_ Out),
a directed vector-labelled graph _𝐺_ = ( _𝑉, 𝐸, 𝐹, 𝜆_ ), and a node _𝑢_ ∈ _𝑉_, we define the output vector
assigned to node _𝑢_ in _𝐺_ by ℜ (written ℜ( _𝐺,𝑢_ )) as follows. First let n _𝑢_ [(][0][)] ≔ _𝜆_ ( _𝑢_ ). For all _𝑖_ ≥ 1, let:


                     -                     n _𝑢_ [(] _[𝑖]_ [)] ≔ Agg n _𝑢_ [(] _[𝑖]_ [−][1][)] _,_ {{(n _𝑣_ [(] _[𝑖]_ [−][1][)] _, 𝜆_ ( _𝑣,𝑢_ )) | ( _𝑣,𝑢_ ) ∈ _𝐸_ }}


If _𝑗_ ≥ 1 is an integer such that n _𝑢_ [(] _[𝑗]_ [)] = n _𝑢_ [(] _[𝑗]_ [−][1][)] for all _𝑢_ ∈ _𝑉_, then ℜ( _𝐺,𝑢_ ) ≔ Out(n _𝑢_ [(] _[𝑗]_ [)] [)][.]

In a RecGNN, the same aggregation function (Agg) is applied recursively until a fixpoint is

reached, at which point an output function (Out) creates the final output vector for each node.

While in practice RecGNNs will often consider a static feature vector and a dynamic state vec
tor [462], we can more concisely encode this as one vector, where part may remain static throughout

the aggregation process representing input features, and part may be dynamically computed repre
senting the state. In practice, Agg and Out are often based on parametric combinations of vectors,

with the parameters learnt based on a sample of output vectors for labelled nodes.


_Example B.61._ The aggregation function for the GNN of Scarselli et al. [462] is given as:


∑︁
Agg(n _𝑢, 𝑁_ ) ≔ _𝑓_ w (n _𝑢,_ n _𝑣,_ a _𝑣𝑢_ )


(n _𝑣,_ a _𝑣𝑢_ ) ∈ _𝑁_


where _𝑓_ w (·) is a contraction function with parameters w. The output function is defined as:


Out (n _𝑢_ ) ≔ _𝑔_ **w** [′] (n _𝑢_ )


where again _𝑔_ w [′] (·) is a function with parameters w [′] . Given a set of nodes labelled with their
expected output vectors, the parameters w and w [′] are learnt.


46Models applying convolutions may differ regarding how edge cases are handled, or on the “stride” of the convolution

applied, where, for example, a stride of 3 for (X ∗ Y) would see the kernel X centred only on elements (Y) _𝑖𝑗_ such that
_𝑖_ mod 3 = 0 and _𝑗_ mod 3 = 0, reducing the number of output elements by a factor of 9. We do not consider such details here.


132


There are notable similarities between graph parallel frameworks (GPFs; see Definition B.48)

and RecGNNs. While we defined GPFs using separate Msg and Agg functions, this is not essential:

conceptually they could be defined in a similar way to RecGNN, with a single Agg function that

“pulls” information from its neighbours (we maintain Msg to more closely reflect how GPFs are

defined/implemented in practice). The key difference between GPFs and GNNs is that in the former,

the functions are defined by the user, while in the latter, the functions are generally learnt from

labelled examples. Another difference arises from the termination condition present in GPFs, though

often the GPF’s termination condition will – like in RecGNNs – reflect convergence to a fixpoint.


Next we abstractly define a non-recursive graph neural network.


_Definition B.62 (Non-recursive graph neural network)._ A _non-recursive graph neural network_
(NRecGNN) with _𝑙_ layers is an _𝑙_ -tuple of functions 𝔑≔ (Agg [(][1][)] _, . . .,_ Agg [(] _[𝑙]_ [)] ), such that, for 1 ≤ _𝑘_ ≤ _𝑙_
(with _𝑎_ 0 _, . . . 𝑎𝑙,𝑏_ ∈ N), Agg [(] _[𝑘]_ [)] : R _[𝑎][𝑘]_ [−][1] × 2 [(][R] _[𝑎𝑘]_ [−][1] [×][R] _[𝑏]_ [)→][N] → R _[𝑎][𝑘]_ .


Each function Agg [(] _[𝑘]_ [)] (as before) computes a new feature vector for a node, given its previous

feature vector and the feature vectors of the nodes and edges forming its neighbourhood. We

assume that _𝑎_ 0 and _𝑏_ correspond to the dimensions of the input node and edge vectors, respectively,
where each function Agg [(] _[𝑘]_ [)] for 2 ≤ _𝑘_ ≤ _𝑙_ accepts as input node vectors of the same dimension
as the output of the function Agg [(] _[𝑘]_ [−][1][)] . Given an NRecGNN 𝔑= (Agg [(][1][)] _, . . .,_ Agg [(] _[𝑙]_ [)] ), a directed
vector-labelled graph _𝐺_ = ( _𝑉, 𝐸, 𝐹, 𝜆_ ), and a node _𝑢_ ∈ _𝑉_, we define the output vector assigned to
node _𝑢_ in _𝐺_ by 𝔑 (written 𝔑( _𝐺,𝑢_ )) as follows. First let n _𝑢_ [(][0][)] ≔ _𝜆_ ( _𝑢_ ). For all _𝑖_ ≥ 1, let:


                                           n _𝑢_ [(] _[𝑖]_ [)] ≔ Agg [(] _[𝑖]_ [)][ �] n _𝑢_ [(] _[𝑖]_ [−][1][)] _,_ {{(n _𝑣_ [(] _[𝑖]_ [−][1][)] _, 𝜆_ ( _𝑣,𝑢_ )) | ( _𝑣,𝑢_ ) ∈ _𝐸_ }}


Then 𝔑( _𝐺,𝑢_ ) ≔ n _𝑢_ [(] _[𝑙]_ [)] [.]

In an _𝑙_ -layer NRecGNN, a different aggregation function can be applied at each step (i.e., in each

layer), up to a fixed number of steps _𝑙_ . We do not consider a separate Out function as it can be
combined with the final aggregation function Agg [(] _[𝑙]_ [)] . When the aggregation functions are based

on a convolutional operator, we call the result a _convolutional graph neural network_ ( _ConvGNN_ ).

We refer to the survey by Wu et al. [559] for discussion of ConvGNNs proposed in the literature.


We have considered GNNs that define the neighbourhood of a node based on its incoming

edges. However, these definitions can be adapted to also consider outgoing neighbours by either

adding inverse edges to the directed vector-labelled graph in pre-processing, or by adding outgoing

neighbours as arguments to the Agg(·) function. More generally, GNNs (and indeed GPFs) relying

solely on the neighbourhood of each node have limited expressivity in terms of their ability to

distinguish nodes and graphs [565]; for example, Barceló et al. [32] show that such NRecGNNs

have a similar expressiveness for classifying nodes as the ALCQ Description Logic discussed

in Section B.5.3. More expressive GNN variants have been proposed that allow the aggregation

functions to access and update a globally shared vector [32]. We refer to the papers by Xu et al. [565]

and Barceló et al. [32] for further discussion on the expressivity of GNNs.


_B.6.4_ _Symbolic learning._ We provide some abstract formal definitions for the tasks of _rule mining_

and _axiom mining_ over graphs, which we generically call _hypothesis mining_ . First we introduce

_hypothesis induction_ : a task that captures a more abstract (ideal) case for hypothesis mining.


_Definition B.63 (Hypothesis induction)._ The task of _hypothesis induction_ assumes a particular
graph entailment relation |=Φ (see Definition B.39; hereafter simply |=). Given _background knowledge_

in the form of a knowledge graph _𝐺_ (a directed edge-labelled graph, possibly extended with rules or
ontologies), a set of _positive edges 𝐸_ [+] such that _𝐺_ does not entail any edge in _𝐸_ [+] (i.e., for all _𝑒_ [+] ∈ _𝐸_ [+],


133


_𝐺_ ̸|= _𝑒_ [+] ) and _𝐸_ [+] does not contradict _𝐺_ (i.e., there is a model of _𝐺_ ∪ _𝐸_ [+] ), and a set of _negative edges_
_𝐸_ [−] such that _𝐺_ does not entail any edge in _𝐸_ [−] (i.e., for all _𝑒_ [−] ∈ _𝐸_ [−], _𝐺_ ̸|= _𝑒_ [−] ), the task is to find a set
of _hypotheses_ (i.e., a set of directed edge-labelled graphs) Ψ such that:

  - _𝐺_ ̸|= _𝜓_ for all _𝜓_ ∈ Ψ (the background knowledge does not entail any hypothesis)

  - _𝐺_ ∪ Ψ [∗] |= _𝐸_ [+] (the background knowledge and hypotheses entail all positive edges);

  - for all _𝑒_ [−] ∈ _𝐸_ [−], _𝐺_ ∪ Ψ [∗] ̸|= _𝑒_ [−] (the background knowledge and hypotheses do not entail any

negative edge);

  - _𝐺_ ∪ Ψ [∗] ∪ _𝐸_ [+] has a model (the background knowledge, hypotheses and positive edges taken

together do not contain a contradiction);

  - for all _𝑒_ [+] ∈ _𝐸_ [+], Ψ [∗] ̸|= _𝑒_ [+] (the hypotheses alone do not entail a positive edge).
where by Ψ [∗] ≔ ∪ _𝜓_ ∈Ψ _𝜓_ we denote the union of all graphs in Ψ.


_Example B.64._ Let us assume ontological entailment |= with semantic conditions Φ as defined in

Tables 3–5. Given the graph of Figure 30 as the background knowledge _𝐺_, along with

  - a set of positive edges _𝐸_ [+] = { [SCL] flight ARI _,_ [SCL] domestic flight ARI }, and

then a set of hypotheses Ψ = { [flight] type Symmetric _,_ [domestic flight] type Symmetric } would entail
all positive edges in _𝐸_ [+] and no negative edges in _𝐸_ [−] when combined with _𝐺_ .


This task represents a somewhat idealised case. Often there is no set of positive edges distinct

from the background knowledge itself. Furthermore, hypotheses not entailing a few positive edges,

or entailing a few negative edges, may still be useful. The task of _hypothesis mining_ rather accepts
as input the background knowledge _𝐺_ and a set of negative edges _𝐸_ [−] (such that for all _𝑒_ [−] ∈ _𝐸_ [−],
_𝐺_ ̸|= _𝑒_ [−] ), and attempts to _score_ individual hypotheses _𝜓_ (such that _𝐺_ ̸|= _𝜓_ ) in terms of their ability
to “explain” _𝐺_ while minimising the number of elements of _𝐸_ [−] entailed by _𝐺_ and _𝜓_ .

We can now abstractly define the task of hypothesis mining.


_Definition B.65 (Hypothesis mining)._ Given a knowledge graph _𝐺_, a set of negative edges _𝐸_ [−],

a scoring function _𝜎_, and a threshold min _𝜎_, the goal of _hypothesis mining_ is to identify a set of
hypotheses { _𝜓_ | _𝐺_ ̸|= _𝜓_ and _𝜎_ ( _𝜓,𝐺, 𝐸_ [−] ) ≥ min _𝜎_ }.


There are two main scoring functions used for _𝜎_ in the literature: _support_ and _confidence_ .


_Definition B.66 (Hypothesis support and confidence)._ Given a knowledge graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ) and

a hypothesis _𝜓_, the _positive support_ of _𝜓_ is defined as follows:


_𝜎_ [+] ( _𝜓,𝐺_ ) ≔ |{ _𝑒_ ∈ _𝐸_ | _𝐺_ [′] ̸|= _𝑒_ and _𝐺_ [′] ∪ _𝜓_ |= _𝑒_ }|


where _𝐺_ [′] denotes _𝐺_ with the edge _𝑒_ removed. Further given a set of negative edges _𝐸_ [−], the _negative_

_support_ of _𝜓_ is defined as follows:


_𝜎_ [−] ( _𝜓,𝐺, 𝐸_ [−] ) ≔ |{ _𝑒_ [−] ∈ _𝐸_ [−] | _𝐺_ ∪ _𝜓_ |= _𝑒_ [−] }|


_𝜎_ [+] ( _𝜓,𝐺_ )
Finally, the _confidence_ of _𝜓_ is defined as _𝜎_ [±] ( _𝜓,𝐺, 𝐸_ [−] ) ≔ _𝜎_ ~~[+]~~ ( _𝜓,𝐺_ )+ _𝜎_ ~~[−]~~ ( _𝜓,𝐺,𝐸_ ~~[−]~~ ) [.]


We have yet to define how the set of negative edges are defined, which, in the context of a

knowledge graph _𝐺_, depends on which assumption is applied:


  - _Closed world assumption (CWA)_ : For any (positive) edge _𝑒_, _𝐺_ ̸|= _𝑒_ if and only if _𝐺_ |= ¬ _𝑒_ . Under

CWA, any edge _𝑒_ not entailed by _𝐺_ can be considered a negative edge.

  - _Open world assumption_ : For a (positive) edge _𝑒_, _𝐺_ ̸|= _𝑒_ does not necessarily imply _𝐺_ |= ¬ _𝑒_ .

Under OWA, the negation of an edge must be entailed by _𝐺_ for it to be considered negative.


134


  - _Partial completeness assumption (PCA)_ : If there exists ( _𝑠, 𝑝,𝑜_ ) such that _𝐺_ |= ( _𝑠, 𝑝,𝑜_ ), then
for all _𝑜_ [′] such that _𝐺_ ̸|= ( _𝑠, 𝑝,𝑜_ [′] ), it holds that _𝐺_ |= ¬( _𝑠, 𝑝,𝑜_ [′] ). Under PCA, if _𝐺_ entails some

outgoing edge(s) labelled _𝑝_ from a node _𝑠_, then such edges are assumed to be complete, and

any edge ( _𝑠, 𝑝,𝑜_ ) not entailed by _𝐺_ can be considered a negative edge.

Knowledge graphs are generally incomplete – in fact, one of the main applications of hypothesis

mining is to try to improve the completeness of the knowledge graph – and thus it would appear

unwise to assume that any edge that is not currently entailed is false/negative. We can thus rule

out CWA. Conversely, under OWA, potentially few (or no) negative edges might be entailed by

the given ontologies/rules, and thus hypotheses may end up having low negative support despite

entailing many edges that do not make sense in practice. Hence the PCA can be adopted as a

heuristic to increase the number of negative edges and apply more sensible scoring of hypotheses.

Different implementations of hypothesis mining may consider different logical languages. Rule

mining, for example, mines hypotheses expressed either as monotonic rules (with positive edges)

or non-monotonic edges (possibly with negated edges). On the other hand, axiom mining considers

hypotheses expressed in a logical language such as Description Logics. Particular implementations

may, for practical reasons, impose further syntactic restrictions on the hypotheses generated, such

as to impose thresholds on their length, on the symbols they use, or on other structural properties

(such as “closed rules” in the case of the AMIE rule mining system [170]; see Section 5.4). Systems

may further implement different search strategies for hypotheses. Systems such as AMIE [170],

RuLES [241], CARL [406], DL-Learner [73], etc., propose _discrete mining_ that recursively generates

candidate formulae through refinement/genetic operators that are then scored and checked for

threshold criteria, thus navigating a branching search space. On the other hand, systems such as

NeuralLP [569] and DRUM [455] apply _differentiable mining_ that allows for learning (path-like)

rules and their scores in a more continuous fashion (e.g., using gradient descent). We refer to

Section 5.4 for further discussion and examples of such techniques for mining hypotheses.


135


