function R = run_analysis(runDynamic, makePlots)
% Recalcula os balanços P25 e, opcionalmente, executa o modelo Simulink.
% run_analysis(false,false) limita a execução aos cálculos estáticos e reduz memória.
if nargin < 1, runDynamic = true; end
if nargin < 2, makePlots = true; end
here = fileparts(mfilename('fullpath'));
projectRoot = fileparts(fileparts(here));
addpath(fullfile(projectRoot, 'matlab', 'funcoes'));
p = read_project_parameters(fullfile(projectRoot, 'dados', 'parametros.csv'));

% Balanço de potência e correntes de operação/placa.
Pg = p.generator_active_mw;
Pm = Pg / p.generator_efficiency;
Paux = p.auxiliary_active_mw;
Pnet = Pg - Paux;
Qg = Pg * tan(acos(p.generator_power_factor));
Qaux = Paux * tan(acos(p.auxiliary_power_factor));
QbeforeCap = Qg - Qaux;
Qnet = QbeforeCap - p.capacitor_bank_mvar;
Snet = hypot(Pnet, Qnet);
Qtarget = Pnet * tan(acos(p.power_factor_target));
QcapRequired = max(0, QbeforeCap - Qtarget);
SgenOperating = hypot(Pg, Qg);
IgenOperating = SgenOperating * 1e6 / (sqrt(3) * p.generator_voltage_kv * 1e3);
IgenRated = p.generator_rating_mva * 1e6 / (sqrt(3) * p.generator_voltage_kv * 1e3);
ItrRatedHV = p.main_transformer_mva * 1e6 / (sqrt(3) * p.grid_voltage_kv * 1e3);
Ipoi = Snet * 1e6 / (sqrt(3) * p.grid_voltage_kv * 1e3);
balance = table(Pg, Pm, Paux, Pnet, Qg, Qaux, p.capacitor_bank_mvar, Qnet, Snet, ...
    Pnet/Snet, Qtarget, QcapRequired, SgenOperating, IgenOperating, IgenRated, ...
    ItrRatedHV, Ipoi, Snet/p.main_transformer_mva, ...
    'VariableNames', {'P_gerador_MW','P_mecanica_MW','P_aux_MW','P_exportada_MW', ...
    'Q_gerador_MVAr','Q_aux_MVAr','Q_banco_MVAr','Q_exportada_MVAr', ...
    'S_exportada_MVA','fp_POI','Q_alvo_fp_MVAr','Q_compensacao_necessaria_MVAr', ...
    'S_gerador_operacao_MVA','I_operacao_gerador_A','I_placa_gerador_A', ...
    'I_transformador_AT_A','I_POI_A','carregamento_trafo_pu'});
writetable(balance, fullfile(projectRoot, 'resultados', 'tabelas', 'balanco-potencia.csv'));

% Curto trifásico de triagem com contribuições fasoriais. X'd é transitória;
% não há X''d, X/R de rede, contribuição de motores ou componente CC.
St = p.main_transformer_mva;
Sg = p.generator_rating_mva;
ZgridT = 1i * St / p.grid_short_circuit_mva;
ZtransformerT = p.main_transformer_r_pu + 1i*p.main_transformer_x_pu;
ZutilityAtGenerator = (ZgridT + ZtransformerT) * St / Sg;
IutilityGenPu = 1 / ZutilityAtGenerator;
ImachineGenPu = 1 / (1i*p.generator_transient_reactance_pu);
ItotalGenPu = IutilityGenPu + ImachineGenPu;
IbaseGen = Sg * 1e6 / (sqrt(3) * p.generator_voltage_kv * 1e3);
IutilityGen = abs(IutilityGenPu) * IbaseGen;
ImachineGen = abs(ImachineGenPu) * IbaseGen;
ItotalGen = abs(ItotalGenPu) * IbaseGen;
SccGen = abs(ItotalGenPu) * Sg;
ZmachineHV = p.main_transformer_r_pu + 1i*(p.main_transformer_x_pu + ...
    p.generator_transient_reactance_pu*Sg/St);
IgridHVPu = 1/ZgridT;
ImachineHVPu = 1/ZmachineHV;
ItotalHVPu = IgridHVPu + ImachineHVPu;
IbaseHV = St * 1e6 / (sqrt(3) * p.grid_voltage_kv * 1e3);
IgridHV = abs(IgridHVPu) * IbaseHV;
ImachineHV = abs(ImachineHVPu) * IbaseHV;
ItotalHV = abs(ItotalHVPu) * IbaseHV;
short = table(Sg, St, St/p.grid_short_circuit_mva, p.main_transformer_r_pu, ...
    p.main_transformer_x_pu, p.generator_transient_reactance_pu, IutilityGen, ...
    ImachineGen, ItotalGen, SccGen, IgridHV, ImachineHV, ItotalHV, ...
    'VariableNames', {'Base_gerador_MVA','Base_transformador_MVA', ...
    'X_rede_na_base_trafo_pu','R_trafo_pu','X_trafo_pu','X_d_transitoria_pu', ...
    'I_rede_13k8_A','I_gerador_13k8_A','I_total_13k8_A','Scc_total_13k8_MVA', ...
    'I_rede_138_A','I_gerador_138_A','I_total_138_A'});
writetable(short, fullfile(projectRoot, 'resultados', 'tabelas', 'curto-circuito.csv'));

% Balanço energético: elétrica bruta e vapor útil permanecem parcelas distintas.
fuel = p.biomass_flow_t_h * 1000 * p.biomass_lhv_mj_kg / 3600;
steam = fuel * p.boiler_efficiency;
annual = fuel * p.annual_operating_hours;
Eel = Pg * p.annual_operating_hours;
Enet = Pnet * p.annual_operating_hours;
Eth = p.process_steam_thermal_mw * p.annual_operating_hours;
utile = (Pg + p.process_steam_thermal_mw) / fuel;
energy = table(fuel, steam, p.process_steam_thermal_mw, Pg, Pnet, utile, annual, ...
    Eel, Enet, Eth, 'VariableNames', {'combustivel_MW','vapor_disponivel_MWth', ...
    'vapor_util_MWth','geracao_bruta_MW','exportacao_liquida_MW', ...
    'rendimento_util_pu','energia_combustivel_MWh_ano','energia_bruta_MWh_ano', ...
    'energia_liquida_MWh_ano','vapor_util_MWhth_ano'});
writetable(energy, fullfile(projectRoot, 'resultados', 'tabelas', 'balanco-energetico.csv'));

R = struct('P_exportada_MW', Pnet, 'Q_exportada_MVAr', Qnet, ...
    'Scc_MVA', SccGen, 'Icc_13k8_A', ItotalGen, 'Icc_138_A', ItotalHV, ...
    'combustivel_MW', fuel, 'rendimento_util_pu', utile, ...
    'energia_liquida_MWh_ano', Enet, 'S_gerador_operacao_MVA', SgenOperating, ...
    'S_gerador_nominal_MVA', Sg, 'I_operacao_gerador_A', IgenOperating, ...
    'I_placa_gerador_A', IgenRated, ...
    'fp_POI', Pnet/Snet, 'Q_compensacao_necessaria_MVAr', QcapRequired);
if ~runDynamic
    R.dinamica = table();
    return
end

% Cenário dinâmico preservado: degrau de potência mecânica e afundamento de tensão.
% O modelo é agregado em pu e não representa cargas de processo ou EMT.
build_model;
mdl = 'modelo_cogeracao_dinamico';
load_system(fullfile(projectRoot, 'simulink', [mdl '.slx']));
t = (0:0.01:5)';
pref = (Pm/Sg)*ones(size(t));
pref(t >= 2.5) = pref(t >= 2.5) + 0.04;
vg = ones(size(t));
vg(t >= 1 & t < 1+p.fault_duration_s) = p.fault_voltage_pu;
vref = ones(size(t));
assignin('base', 'u_ts', timeseries([pref vg vref zeros(size(t))], t));
simout = sim(mdl, 'StopTime', '5', 'ReturnWorkspaceOutputs', 'on');
log = simout.get('y_log');
data = squeeze(log.Data);
if size(data,1) ~= numel(log.Time) && size(data,2) == numel(log.Time), data = data'; end
speed = data(:,2);
Pe = data(:,4);
Q = data(:,6);
Vt = data(:,7);
frequency = p.frequency_hz * (1 + speed);
currentPu = hypot(Pe,Q) ./ max(Vt,0.1);
currentA = currentPu * Sg*1e6 / (sqrt(3)*p.generator_voltage_kv*1e3);
dyn = table(log.Time,data(:,1),speed,data(:,3),Pe,data(:,5),Q,Vt,frequency,currentPu,currentA, ...
    'VariableNames', {'time_s','angle_rad','speed_deviation_pu','Pm_pu','Pe_pu', ...
    'Efd_deviation_pu','Q_pu','Vt_pu','frequency_Hz','I_pu','I_gerador_A'});
writetable(dyn, fullfile(projectRoot, 'resultados', 'tabelas', 'dinamica-maquina.csv'));
R.dinamica = dyn;

if makePlots
    fig = figure('Visible','off');
    tiledlayout(4,1);
    nexttile; plot(dyn.time_s,dyn.Vt_pu,'LineWidth',1.1); grid on; ylabel('Vt (pu)');
    title('Resposta agregada a afundamento de tensão e degrau de potência mecânica');
    nexttile; plot(dyn.time_s,dyn.frequency_Hz,'LineWidth',1.1); grid on; ylabel('f (Hz)');
    nexttile; plot(dyn.time_s,dyn.Pe_pu*Sg,dyn.time_s,dyn.Q_pu*Sg,'LineWidth',1.1); grid on; ylabel('P / Q (MW / MVAr)');
    legend('P elétrica','Q elétrica','Location','best');
    nexttile; plot(dyn.time_s,dyn.I_gerador_A,'LineWidth',1.1); grid on; ylabel('I (A)'); xlabel('Tempo (s)');
    exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','resposta-dinamica.png'));
    close(fig);
    fig = figure('Visible','off');
    bar([Pg Pnet Paux p.process_steam_thermal_mw fuel]);
    xticklabels({'Geração bruta','Exportação líquida','Auxiliares','Vapor útil','Combustível'});
    ylabel('MW / MWth'); grid on; title('Balanço energético nominal');
    exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','balanco-energetico.png'));
    close(fig);
end
end
