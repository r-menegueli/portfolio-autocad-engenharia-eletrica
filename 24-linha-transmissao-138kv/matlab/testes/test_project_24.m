function test_project_24(R)
if nargin<1, R=run_analysis; end
assert(height(R.eletrico)==3 && height(R.estruturas)==101); assert(R.GMD_m>9 && R.GMD_m<10);
assert(all(isfinite(R.eletrico.V_envio_LL_kV)) && all(R.mecanico.flecha_vertical_m>0));
assert(R.ampacidade_A>0 && R.ampacidade_A<1000); assert(R.Imax_A>0 && R.overload==(R.Imax_A>R.ampacidade_A));
fprintf('P24: fluxo, flecha, estruturas e equilíbrio térmico verificados.\n');
end
