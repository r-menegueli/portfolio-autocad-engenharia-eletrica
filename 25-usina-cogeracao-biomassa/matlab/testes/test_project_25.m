function test_project_25(R)
if nargin<1, R=run_analysis; end
assert(abs(R.P_exportada_MW-22.8)<1e-9); assert(R.Q_exportada_MVAr>0 && R.Q_exportada_MVAr<12);
assert(R.Scc_MVA>150 && R.Scc_MVA<300); assert(R.combustivel_MW>100 && R.combustivel_MW<110);
assert(R.rendimento_util_pu>0.4 && R.rendimento_util_pu<0.7); assert(R.energia_liquida_MWh_ano>160000);
assert(all(isfinite(R.dinamica.speed_deviation_pu))); assert(height(R.dinamica)>50);
assert(max(abs(R.dinamica.speed_deviation_pu))<0.05); assert(max(R.dinamica.Efd_deviation_pu)<0.3);
fprintf('P25: potência, curto, energia e dinâmica verificados.\n');
end
