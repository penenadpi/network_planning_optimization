param nS;
param nL;
set S:=1..nS;
set L:=1..nL;

 
param Capacity {s in S};   
param Demand {l in L};

param S_Cost {s in S};
param M_Cost {s in S};
param E_Cost {s in S};  
param D_Cost {l in L};    

param Pout {s in S, l in L}; 
param LCR {s in S, l in L}; 
param CC {s in S, l in L}; 

param T_Pout {l in L}; 
param T_LCR {l in L}; 
param T_CC {l in L}; 

# variable declaration
var X {s in S, l in L} binary;

# objective function
minimize cost:
	sum{s in S, l in L} X[s,l]*(S_Cost[s]+E_Cost[s]+M_Cost[s]+D_Cost[l]); 
	 
# constraints
subject to alloc_constraint1 {l in L}:
	sum{s in S}X[s,l]=1;
subject to alloc_constraint2 {s in S}:
	sum{l in L}X[s,l]<=1;
	
subject to alloc_constraint3 {l in L}:
	sum{l in L}X[s,l]*Pout<=T_Pout;
subject to alloc_constraint4 {l in L}:
	sum{l in L}X[s,l]*T_CC>=T_CC;
subject to alloc_constraint5 {l in L}:
	sum{l in L}X[s,l]*T_LCR>=T_LCR;	
subject to demand_constraint {l in L}:
	sum{s in S}(X[s,l]*Capacity[s])>=Demand[l];