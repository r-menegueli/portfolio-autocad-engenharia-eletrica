function test_project_23(R)
if nargin<1, R=run_analysis; end
assert(abs(R.P_MW-28)<1e-9); assert(R.Q_STATCOM_MVAr>=0 && R.Q_STATCOM_MVAr<=12.5);
assert(R.Icc_34k5_kA>4 && R.Icc_34k5_kA<7); assert(R.THDi_sintetico>0.2 && R.THDi_sintetico<0.3);
if ~isempty(R.dinamica)
    assert(all(isfinite(R.dinamica.V_pu))); assert(height(R.dinamica)>50);
    fprintf('P23: balanço, curto, harmônicos e série dinâmica verificados.\n');
else
    fprintf('P23: balanço, curto e harmônicos verificados; dinâmica não executada.\n');
end
end
