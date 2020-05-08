%--------------------------------------------------------------------------
% File     : ALG202+1 : TPTP v7.2.0. Released v2.7.0.
% Domain   : General Algebra
% Problem  : Quasigroups 7 QG5: CPROPS-SORTED-DISCRIMINANT-PROBLEM-2
% Version  : Especial.
% English  :

% Refs     : [Mei03] Meier (2003), Email to G.Sutcliffe
%          : [CM+04] Colton et al. (2004), Automatic Generation of Classifi
% Source   : [Mei03]
% Names    :

% Status   : Theorem
% Rating   : 0.03 v7.1.0, 0.04 v7.0.0, 0.07 v6.4.0, 0.12 v6.3.0, 0.04 v6.2.0, 0.08 v6.1.0, 0.10 v6.0.0, 0.04 v5.5.0, 0.07 v5.4.0, 0.11 v5.3.0, 0.19 v5.2.0, 0.05 v5.0.0, 0.08 v4.1.0, 0.09 v4.0.0, 0.08 v3.7.0, 0.00 v3.4.0, 0.05 v3.3.0, 0.07 v3.2.0, 0.18 v3.1.0, 0.11 v2.7.0
% Syntax   : Number of formulae    :    5 (   0 unit)
%            Number of atoms       :   24 (   6 equality)
%            Maximal formula depth :    9 (   5 average)
%            Number of connectives :   21 (   2   ~;   0   |;   4   &)
%                                         (   0 <=>;  15  =>;   0  <=;   0 <~>)
%                                         (   0  ~|;   0  ~&)
%            Number of predicates  :    3 (   0 propositional; 1-2 arity)
%            Number of functors    :    4 (   0 constant; 1-2 arity)
%            Number of variables   :   14 (   0 sgn;  14   !;   0   ?)
%            Maximal term depth    :    3 (   2 average)
% SPC      : FOF_THM_RFO_SEQ

% Comments :
%--------------------------------------------------------------------------
fof(ax1,axiom,(
    ! [U] :
      ( sorti1(U)
     => ! [V] :
          ( sorti1(V)
         => sorti1(op1(U,V)) ) ) )).

fof(ax2,axiom,(
    ! [U] :
      ( sorti2(U)
     => ! [V] :
          ( sorti2(V)
         => sorti2(op2(U,V)) ) ) )).

fof(ax3,axiom,(
    ! [U] :
      ( sorti1(U)
     => op1(U,U) = U ) )).

fof(ax4,axiom,(
    ~ ! [U] :
        ( sorti2(U)
       => op2(U,U) = U ) )).

fof(co1,conjecture,
    ( ( ! [U] :
          ( sorti1(U)
         => sorti2(h(U)) )
      & ! [V] :
          ( sorti2(V)
         => sorti1(j(V)) ) )
   => ~ ( ! [W] :
            ( sorti1(W)
           => ! [X] :
                ( sorti1(X)
               => h(op1(W,X)) = op2(h(W),h(X)) ) )
        & ! [Y] :
            ( sorti2(Y)
           => ! [Z] :
                ( sorti2(Z)
               => j(op2(Y,Z)) = op1(j(Y),j(Z)) ) )
        & ! [X1] :
            ( sorti2(X1)
           => h(j(X1)) = X1 )
        & ! [X2] :
            ( sorti1(X2)
           => j(h(X2)) = X2 ) ) )).

%--------------------------------------------------------------------------
