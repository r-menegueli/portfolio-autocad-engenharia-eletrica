function test_project_24(R)
if nargin<1, R=run_analysis(false); end
assert(height(R.eletrico)==9 && height(R.estruturas)==101);
assert(height(R.mecanico)==900 && height(R.ampacidade)==9);
assert(R.GMD_m>9 && R.GMD_m<10 && R.GMR_feixe_m>0);

% All nine independent load/power-factor pairs must be present and finite.
assert(numel(unique(R.eletrico.P_MW))==3 && numel(unique(R.eletrico.fp))==3);
assert(all(isfinite(R.eletrico.V_envio_LL_kV)) && all(R.eletrico.I_recebimento_A>0));
assert(all(abs(R.eletrico.P_envio_MW-R.eletrico.P_MW-R.eletrico.perdas_MW)<1e-9));
apparentFromVI=sqrt(3)*138*R.eletrico.I_recebimento_A/1000;
assert(all(abs(apparentFromVI-R.eletrico.S_MVA)<1e-8));

% 100 spans x 3 conductor temperatures x 3 winds; route length closes at 30 km.
assert(all(R.mecanico.flecha_vertical_m>0));
assert(all(R.mecanico.flecha_transversal_m>=0));
assert(all(R.mecanico.flecha_resultante_m>=R.mecanico.flecha_vertical_m));
assert(any(R.mecanico.flecha_transversal_m>1));
assert(numel(unique(R.mecanico.vao_inicial))==100);
assert(abs(sum(R.estruturas.vao_ate_proxima_estrutura_m)-30000)<1e-9);
assert(R.estruturas.vao_ate_proxima_estrutura_m(end)==0);
anchorStations=[0 9.9 20.1 30.0];
actualAnchors=R.estruturas.km(R.estruturas.tipo=="ancoragem");
assert(isequal(actualAnchors(:)',anchorStations));

% Nine independent ambient/wind pairs and screening status are reported.
assert(numel(unique(R.ampacidade.ambiente_C))==3);
assert(numel(unique(R.ampacidade.vento_m_s))==3);
assert(all(R.ampacidade.ampacidade_feixe_A>0));
assert(R.ampacidade_A==min(R.ampacidade.ampacidade_feixe_A));
assert(R.Imax_A>0 && R.overload==(R.Imax_A>R.ampacidade_A));
assert(R.margem_termica_minima_percentual==min(R.ampacidade.margem_percentual));
fprintf('P24: 9 casos eletricos, 900 casos mecanicos, 9 casos termicos e 101 estruturas verificados.\n');
end
