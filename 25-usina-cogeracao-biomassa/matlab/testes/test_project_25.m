function test_project_25(R)
if nargin<1, R=run_analysis; end
assert(abs(R.P_exportada_MW-22.8)<1e-9);
assert(R.Q_exportada_MVAr>0 && R.fp_POI>=0.95);
assert(R.S_gerador_operacao_MVA<R.S_gerador_nominal_MVA);
assert(R.I_operacao_gerador_A<R.I_placa_gerador_A);
assert(R.Q_compensacao_necessaria_MVAr>0);
assert(R.Scc_MVA>300 && R.Scc_MVA<350);
assert(R.Icc_138_A>20000 && R.Icc_138_A<23000);
assert(R.combustivel_MW>100 && R.combustivel_MW<110);
assert(R.rendimento_util_pu>0.4 && R.rendimento_util_pu<0.7);
assert(R.energia_liquida_MWh_ano>160000);
if ~isempty(R.dinamica)
    assert(all(isfinite(R.dinamica.speed_deviation_pu))); assert(height(R.dinamica)>50);
    assert(all(isfinite(R.dinamica.frequency_Hz)) && all(R.dinamica.I_gerador_A>=0));
    assert(max(abs(R.dinamica.speed_deviation_pu))<0.05);
    assert(max(R.dinamica.Efd_deviation_pu)<0.3);
    fprintf('P25: balanços, bases de curto, energia e série dinâmica verificados.\n');
else
    fprintf('P25: balanços, bases de curto e energia verificados; dinâmica não executada.\n');
end
end
