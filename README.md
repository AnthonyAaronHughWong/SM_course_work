#*My Stochastic Signal Modeling Course Work*


##Languages

I used `R`, `Haskell` and `Python`.
Their suffix is `.R`, `.hs` and `.py`
respectively.

You need `Python3.5` to run my Python code, and
`GHC` to compile my Haskell code.

Normally, I try best not to use standard library.

##File Structure

###Input Files
I manually stripped comma and bracket from
`train.txt` and `test.txt`, and separated
samples from `A` and `B` to ease my code from
reading them, resulting in `trainA.txt`,
`trainB.txt`, `testA.txt` and `testB.txt`.

###Source Files

sed.sh:
~ remove punctuation from Input File.

visualize.R:
~ visualize data interactively using `R` language.

Q1.hs:
~ **Problem One** source code.

README.md:
~ Used to generate this report.

report.pdf:
~ The report you should be reading now.

Makefile:
~ Use `make` to compile necessary files. It's
mainly meant for the `Haskell` source and generating
this report in `pdf` format, since `Python`
and `R` don't need to be compiled.
Hit `Tab` and your
shell may give you a list of targets.

Otherfiles:
~ They are mostly source files that will be imported by other files.


##Problems

%math definations here
\newcommand{\norm}[3]{
  \frac{1}{
#3\sqrt{2\pi}
}\,
e^{-\frac{(#1 - #2)^2}
  {2 #3^2}}
  }

\newcommand{\normal}[0]{
\frac{1}{
\sigma\sqrt{2\pi}
}\,
e^{-\frac{(x - \mu)^2}
  {2 \sigma^2}}
}

###Q1

This is easy. Given $\mathbf{x}$ as a list of  $n$ samples:

$$mean = \frac{
\sum_{x \in \mathbf{x}}
	{x}}
{n}$$


$$deviation = \frac{
\sum_{x \in \mathbf{x}}
	{(x - mean)^2}}
{n}$$



$$pdf = 
\norm{x}{\mu}{\sigma}
$$

At the first, I made the mistake to used the `deviation`
of the samples
as the `standard deviation` in the model.
So it got squared twice when classifying,
resulting in high error rate. But I found this bug eventually.

###Q2

I assume every sample has the responsibilities of every model as hidden variable.


####First Approach
The kmeans works pretty good once I wrote it,
but the gmm always produce models with very similiar centers.
However by looking at the visualization of the data, I don't
think it's a single gauss model.

####Bug finding
Okay, something is wrong. I found that my deviations are all too large. So they all produce pretty
similiar probabilities.

Another problem is, the numeric calculation is not robust. Sometimes it produces `Nan`, but it
doesn't happen often, and I havn't found a solution.

####Result
I should say it doesn't improve very much, though. Maybe I did it wrong?


###Q3

We are supposed to use discrimitive method, then the objective function should be
the Classification Error Probability which we should minimize.
Given $x$ as a sample, and $i$ as the index of classes from set $C$,

\newcommand{\normi}[1]{
  \norm{x}{\mu_{#1}}{\sigma_{#1}}}

$$p(i|x)=\frac{
  \normi{i}}{
  \sum_{j \in C}{\normi{j}}
}
$$

Then the decision is made by:

\newcommand{\argmax}{\operatornamewithlimits{argmax}}

$$
k(x) = \argmax_i p(i|x)
$$

So I guess I'm supposed to use
the empirical classification error,
given $c$ as the true class,
which is:

\newcommand{\length}{\#}

$$
\frac{
\length\{k(x) \ne c(x)\, \forall x \in \mathbf{x}  \}
}{
\length(\mathbf{x})
}$$

This function needs lots of time to calculate for sure.
But I found in the PPTs that `Q` can be approximated:


\newcommand{\stepAppr}[2]{
\frac{1}{1 + e ^ {- #1#2 }}
}



$$
Q(\lambda)=\sum_{x}{
\stepAppr{\alpha}{d(x,c(x))}
}$$

with

$$
d(x,c)=-ln(p(c)p(x|\lambda_{c}))+ln(
\frac{1}{\length{\mathbf{x}}-1}
\sum_{c' \neq c }
{e ^{
\eta \cdot  ln(p(c')p(x|\lambda_{c'}))
}})^{\frac{1}{\eta}}
$$

where $\alpha$ and $\eta > 1$ are parameters.
Then

$$
\frac{\partial}{\partial\lambda}Q=
\sum_{x}{
\alpha\stepAppr{\alpha}{d}(1-\stepAppr{\alpha}{d}) \cdot
\frac{\partial d}{\partial\lambda}
}$$
