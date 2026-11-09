function R = run_analysis(makePlots)
% Reproducible screening calculations for the conceptual 138 kV line.
% Load, power-factor and weather combinations are evaluated independently.
% Set makePlots=false on memory-constrained hosts; tables and report are still produced.
if nargin < 1
    makePlots = true;
end
here = fileparts(mfilename('fullpath'));
projectRoot = fileparts(fileparts(here));
addpath(fullfile(projectRoot, 'matlab', 'funcoes'));
p = read_project_parameters(fullfile(projectRoot, 'dados', 'parametros.csv'));

% Positive-sequence medium-line model with a two-conductor bundle per phase.
f = p.frequency_hz;
Lkm = p.length_km;
L = Lkm*1000;
Vll = p.voltage_kv*1000;
phasePosition = [p.phase_spacing_m_1, p.phase_spacing_m_2, p.phase_spacing_m_3];
phaseDistance = [abs(phasePosition(2)-phasePosition(1)), ...
    abs(phasePosition(3)-phasePosition(2)), abs(phasePosition(3)-phasePosition(1))];
GMD = prod(phaseDistance)^(1/3);
nSub = p.bundle_subconductors;
if nSub ~= 2
    error('Este modelo foi implementado para dois subconductores por fase.');
end
bundleSpacing = p.bundle_spacing_m;
GMRbundle = sqrt(p.conductor_gmr_m*bundleSpacing);
radiusBundle = sqrt((p.conductor_diameter_m/2)*bundleSpacing);
Lpkm = 2e-4*log(GMD/GMRbundle); % H/km
Cpm = 2*pi*8.8541878128e-12/log(GMD/radiusBundle); % F/m
Rphase75 = p.conductor_rac75_ohm_km/nSub; % ohm/km
Z = (Rphase75+1i*2*pi*f*Lpkm)*Lkm;
Y = 1i*2*pi*f*Cpm*L;
A = 1+Y*Z/2;
B = Z*(1+Y*Z/4);
C = Y*(1+Y*Z/4);
D = A;

% Full 3 x 3 sensitivity: each active load is combined with each power factor.
loads = [p.load_active_mw_1, p.load_active_mw_2, p.load_active_mw_3];
pfs = [p.load_power_factor_1, p.load_power_factor_2, p.load_power_factor_3];
[loadGrid,pfGrid] = ndgrid(loads,pfs);
Pload = loadGrid(:);
pfLoad = pfGrid(:);
nElectrical = numel(Pload);
Qrecv = Pload.*tan(acos(pfLoad));
Srecv = hypot(Pload,Qrecv);
Irecv = zeros(nElectrical,1);
Vsend = zeros(nElectrical,1);
regulation = zeros(nElectrical,1);
Psend = zeros(nElectrical,1);
losses = zeros(nElectrical,1);
Vr = Vll/sqrt(3);
for k = 1:nElectrical
    Ir = conj((Pload(k)+1i*Qrecv(k))*1e6/(3*Vr));
    Vs = A*Vr+B*Ir;
    Is = C*Vr+D*Ir;
    Irecv(k) = abs(Ir);
    Vsend(k) = sqrt(3)*abs(Vs)/1000;
    regulation(k) = 100*(Vsend(k)-p.voltage_kv)/p.voltage_kv;
    Psend(k) = 3*real(Vs*conj(Is))/1e6;
    losses(k) = Psend(k)-Pload(k);
end
electrical = table(Pload,pfLoad,Srecv,Irecv,Vsend,regulation,Psend,losses, ...
    'VariableNames',{'P_MW','fp','S_MVA','I_recebimento_A','V_envio_LL_kV', ...
    'regulacao_percentual','P_envio_MW','perdas_MW'});
writetable(electrical,fullfile(projectRoot,'resultados','tabelas','resultados-eletricos.csv'));
Imax = max(Irecv);

% Fictitious route: local X east / Y north, origin at SE A; stations are synthetic.
routeKm = [p.route_km_1 p.route_km_2 p.route_km_3 p.route_km_4 p.route_km_5 ...
    p.route_km_6 p.route_km_7 p.route_km_8 p.route_km_9 p.route_km_10 ...
    p.route_km_11 p.route_km_12 p.route_km_13 p.route_km_14 p.route_km_15 p.route_km_16];
routeElevation = [p.route_elevation_m_1 p.route_elevation_m_2 p.route_elevation_m_3 ...
    p.route_elevation_m_4 p.route_elevation_m_5 p.route_elevation_m_6 ...
    p.route_elevation_m_7 p.route_elevation_m_8 p.route_elevation_m_9 ...
    p.route_elevation_m_10 p.route_elevation_m_11 p.route_elevation_m_12 ...
    p.route_elevation_m_13 p.route_elevation_m_14 p.route_elevation_m_15 p.route_elevation_m_16];
routeBearing = [p.route_bearing_deg_1 p.route_bearing_deg_2 p.route_bearing_deg_3 ...
    p.route_bearing_deg_4 p.route_bearing_deg_5 p.route_bearing_deg_6 ...
    p.route_bearing_deg_7 p.route_bearing_deg_8 p.route_bearing_deg_9 ...
    p.route_bearing_deg_10 p.route_bearing_deg_11 p.route_bearing_deg_12 ...
    p.route_bearing_deg_13 p.route_bearing_deg_14 p.route_bearing_deg_15 p.route_bearing_deg_16];
anchorKm = [p.anchor_stations_km_1 p.anchor_stations_km_2 ...
    p.anchor_stations_km_3 p.anchor_stations_km_4];
nSpan = round(L/p.span_m);
if abs(nSpan*p.span_m-L)>1e-6
    error('Comprimento total nao fecha com vaos inteiros de referencia.');
end
span = L/nSpan;
stationM = (0:nSpan)'*span;
stationKm = stationM/1000;
elevation = interp1(routeKm,routeElevation,stationKm,'linear');
bearing = interp1(routeKm,routeBearing,(stationKm(1:end-1)+stationKm(2:end))/2,'linear');
east = [0;cumsum(span*cosd(bearing(:)))];
north = [0;cumsum(span*sind(bearing(:)))];
structureType = repmat("suspensao",nSpan+1,1);
anchorIndex = round(anchorKm*1000/span)+1;
if any(abs(stationKm(anchorIndex)-anchorKm(:))>0.0005)
    error('Estacao de ancoragem nao coincide com estaca de estrutura.');
end
structureType(anchorIndex) = repmat("ancoragem",numel(anchorIndex),1);
spanToNext = [diff(stationM);0];
structures = table((0:nSpan)',stationKm,east,north,elevation,structureType,spanToNext, ...
    'VariableNames',{'estrutura','km','X_local_m','Y_local_m','elevacao_sintetica_m', ...
    'tipo','vao_ate_proxima_estrutura_m'});
writetable(structures,fullfile(projectRoot,'resultados','tabelas','tabela-estruturas.csv'));

% Parabolic sag-tension screen: independent conductor-temperature/wind combinations.
mechanicalTemps = [p.mechanical_conductor_temperatures_c_1, ...
    p.mechanical_conductor_temperatures_c_2, p.mechanical_conductor_temperatures_c_3];
mechanicalWinds = [p.mechanical_wind_speeds_m_s_1, ...
    p.mechanical_wind_speeds_m_s_2, p.mechanical_wind_speeds_m_s_3];
[tempGrid,windGrid] = ndgrid(mechanicalTemps,mechanicalWinds);
nMechanical = nSpan*numel(tempGrid);
mechTemperature = zeros(nMechanical,1);
mechWind = zeros(nMechanical,1);
mechSpan = zeros(nMechanical,1);
mechH = zeros(nMechanical,1);
mechSag = zeros(nMechanical,1);
mechLateralSag = zeros(nMechanical,1);
mechResultantSag = zeros(nMechanical,1);
mechClearance = zeros(nMechanical,1);
mechSupportTension = zeros(nMechanical,1);
mechTensionRatio = zeros(nMechanical,1);
row = 0;
for c = 1:numel(tempGrid)
    [sagVertical,sagResultant,horizontalTension,supportTension] = ...
        span_state(p,span,tempGrid(c),windGrid(c));
    windLoad = 0.5*p.air_density_kg_m3*p.drag_coefficient* ...
        p.conductor_diameter_m*windGrid(c)^2;
    for j = 1:nSpan
        tRoute = (routeKm*1000-stationM(j))/span;
        tRoute = tRoute(tRoute>0 & tRoute<1);
        t = unique([linspace(0,1,51),tRoute]);
        ground = interp1(routeKm*1000,routeElevation,stationM(j)+span*t,'linear');
        attachment = (elevation(j)+p.mean_conductor_height_m)*(1-t) + ...
            (elevation(j+1)+p.mean_conductor_height_m)*t;
        clearanceAt = attachment-sagVertical*4*t.*(1-t)-ground;
        row = row+1;
        mechTemperature(row) = tempGrid(c);
        mechWind(row) = windGrid(c);
        mechSpan(row) = j;
        mechH(row) = horizontalTension/1000;
        mechSag(row) = sagVertical;
        mechLateralSag(row) = windLoad*span^2/(8*horizontalTension);
        mechResultantSag(row) = sagResultant;
        mechClearance(row) = min(clearanceAt);
        mechSupportTension(row) = supportTension/1000;
        mechTensionRatio(row) = supportTension/p.conductor_rated_tensile_n;
    end
end
mechanical = table(mechTemperature,mechWind,mechSpan,mechH,mechSag, ...
    mechLateralSag,mechResultantSag,mechClearance, ...
    mechSupportTension,mechTensionRatio, ...
    'VariableNames',{'temperatura_condutor_C','vento_m_s','vao_inicial', ...
    'tracao_horizontal_kN','flecha_vertical_m','flecha_transversal_m', ...
    'flecha_resultante_m','clearance_minimo_sintetico_m', ...
    'tracao_no_apoio_kN','fracao_carga_ruptura'});
writetable(mechanical,fullfile(projectRoot,'resultados','tabelas','resultados-mecanicos.csv'));

% Thermal screen: all ambient-temperature/wind pairs, 75 C conductor limit.
ambientTemps = [p.ambient_temperatures_c_1,p.ambient_temperatures_c_2,p.ambient_temperatures_c_3];
thermalWinds = [p.wind_speeds_m_s_1,p.wind_speeds_m_s_2,p.wind_speeds_m_s_3];
[ambientGrid,thermalWindGrid] = ndgrid(ambientTemps,thermalWinds);
nThermal = numel(ambientGrid);
ampacitySub = zeros(nThermal,1);
ampacityBundle = zeros(nThermal,1);
hConv = zeros(nThermal,1);
qSolar = zeros(nThermal,1);
qConvection = zeros(nThermal,1);
qRadiation = zeros(nThermal,1);
for k = 1:nThermal
    deltaT = p.conductor_temperature_limit_c-ambientGrid(k);
    hConv(k) = max(p.thermal_natural_h_w_m2_c, ...
        p.thermal_h_w_m2_c*sqrt(thermalWindGrid(k)/p.thermal_reference_wind_m_s));
    qSolar(k) = p.solar_absorptivity*p.solar_flux_w_m2*p.conductor_diameter_m;
    qConvection(k) = pi*p.conductor_diameter_m*hConv(k)*deltaT;
    sigma = 5.670374419e-8;
    qRadiation(k) = pi*p.conductor_diameter_m*0.5*sigma* ...
        ((p.conductor_temperature_limit_c+273.15)^4-(ambientGrid(k)+273.15)^4);
    qNet = qConvection(k)+qRadiation(k)-qSolar(k);
    ampacitySub(k) = sqrt(max(0,qNet)/(p.conductor_rac75_ohm_km/1000));
    ampacityBundle(k) = nSub*ampacitySub(k);
end
thermalMargin = 100*(ampacityBundle-Imax)./ampacityBundle;
thermalStatus = repmat("PASS_SCREEN",nThermal,1);
thermalStatus(Imax>ampacityBundle) = "EXCEEDS_SCREEN";
thermal = table(ambientGrid(:),thermalWindGrid(:), ...
    repmat(p.conductor_temperature_limit_c,nThermal,1),hConv,qSolar,qConvection, ...
    qRadiation,ampacitySub,ampacityBundle,repmat(Imax,nThermal,1), ...
    thermalMargin,thermalStatus, ...
    'VariableNames',{'ambiente_C','vento_m_s','limite_condutor_C', ...
    'h_conveccao_assumido_W_m2K','calor_solar_W_m','conveccao_W_m','radiacao_W_m', ...
    'ampacidade_por_subcondutor_A','ampacidade_feixe_A','I_max_nove_casos_A', ...
    'margem_percentual','status_triagem'});
writetable(thermal,fullfile(projectRoot,'resultados','tabelas','ampacidade-estimada.csv'));

% Load/loss and thermal sensitivity plots.
if makePlots
fig = figure('Visible','off');
tiledlayout(2,1);
nexttile;
plot(Pload,Irecv,'o','LineWidth',1.1); grid on;
xlabel('Carga ativa recebida (MW)'); ylabel('Corrente (A)');
title('Corrente nos nove pares de carga e fator de potência');
nexttile;
for pf = sort(pfs)
    pick = abs(pfLoad-pf)<1e-12;
    plot(Pload(pick),losses(pick),'o-','DisplayName',sprintf('fp %.2f',pf)); hold on;
end
grid on; legend('Location','best');
xlabel('Carga ativa recebida (MW)'); ylabel('Perdas estimadas (MW)');
title('Perdas versus carga, agrupadas por fator de potência');
exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','operacao-eletrica.png')); close(fig);
fprintf('Grafico 1/6 salvo: operacao-eletrica.png\n');

fig = figure('Visible','off');
tiledlayout(1,2);
nexttile;
plot(ambientGrid(:),ampacityBundle,'o','LineWidth',1.1); hold on;
yline(Imax,'--r','I_{max}'); grid on;
xlabel('Temperatura ambiente (°C)'); ylabel('Ampacidade do feixe (A)'); title('Triagem térmica');
nexttile;
plot(thermalWindGrid(:),thermalMargin,'o','LineWidth',1.1); yline(0,'--r'); grid on;
xlabel('Vento transversal (m/s)'); ylabel('Margem (%)'); title('Margem por condição ambiental');
exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','triagem-termica.png')); close(fig);
fprintf('Grafico 2/6 salvo: triagem-termica.png\n');

% Sag and support-tension plots.
fig = figure('Visible','off');
tiledlayout(1,3);
nexttile;
for wi = mechanicalWinds
    sagVerticalAtTemp = zeros(size(mechanicalTemps));
    for ti = 1:numel(mechanicalTemps)
        sagVerticalAtTemp(ti) = span_state(p,span,mechanicalTemps(ti),wi);
    end
    plot(mechanicalTemps,sagVerticalAtTemp,'o-', ...
        'DisplayName',sprintf('%.2g m/s',wi)); hold on;
end
grid on; legend('Location','best');
xlabel('Temperatura do condutor (°C)'); ylabel('Flecha vertical (m)'); title('Componente vertical');
nexttile;
for wi = mechanicalWinds
    lateralAtTemp = zeros(size(mechanicalTemps));
    windLoad = 0.5*p.air_density_kg_m3*p.drag_coefficient*p.conductor_diameter_m*wi^2;
    for ti = 1:numel(mechanicalTemps)
        [~,~,hAtTemp] = span_state(p,span,mechanicalTemps(ti),wi);
        lateralAtTemp(ti) = windLoad*span^2/(8*hAtTemp);
    end
    plot(mechanicalTemps,lateralAtTemp,'o-', ...
        'DisplayName',sprintf('%.2g m/s',wi)); hold on;
end
grid on; legend('Location','best');
xlabel('Temperatura do condutor (°C)'); ylabel('Flecha transversal (m)'); title('Componente pelo vento');
nexttile;
for wi = mechanicalWinds
    tensionAtWind = zeros(size(mechanicalTemps));
    for ti = 1:numel(mechanicalTemps)
        [~,~,~,tensionAtWind(ti)] = span_state(p,span,mechanicalTemps(ti),wi);
    end
    plot(mechanicalTemps,tensionAtWind/1000,'o-', ...
        'DisplayName',sprintf('%.2g m/s',wi)); hold on;
end
grid on; xlabel('Temperatura do condutor (°C)'); ylabel('Tração no apoio (kN)');
title('Tração mecânica'); legend('Location','best');
exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','flecha-tracao.png')); close(fig);
fprintf('Grafico 3/6 salvo: flecha-tracao.png\n');

% Approximate line-voltage profile for 140 MW over power-factor cases.
fig = figure('Visible','off');
Pdesign = max(loads);
for pf = sort(pfs)
    Qdesign = Pdesign*tan(acos(pf));
    Idesign = conj((Pdesign+1i*Qdesign)*1e6/(3*Vr));
    distances = linspace(0,1,61);
    Vprofile = zeros(size(distances));
    for k = 1:numel(distances)
        zPart = (Rphase75+1i*2*pi*f*Lpkm)*Lkm*distances(k);
        yPart = 1i*2*pi*f*Cpm*L*distances(k);
        aPart = 1+yPart*zPart/2;
        bPart = zPart*(1+yPart*zPart/4);
        Vprofile(k) = sqrt(3)*abs(aPart*Vr+bPart*Idesign)/1000;
    end
    plot(distances*Lkm,Vprofile,'DisplayName',sprintf('fp %.2f',pf)); hold on;
end
grid on; xlabel('Distância a partir do terminal receptor (km)');
ylabel('Tensão linha-linha (kV)'); title('Perfil aproximado por segmentos do modelo nominal π');
legend('Location','best');
exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','perfil-tensao.png')); close(fig);
fprintf('Grafico 4/6 salvo: perfil-tensao.png\n');

fig = figure('Visible','off');
for loadMW = sort(loads)
    pick = abs(Pload-loadMW)<1e-12;
    plot(pfLoad(pick),losses(pick),'o-','DisplayName',sprintf('P %.0f MW',loadMW)); hold on;
end
grid on; legend('Location','best');
xlabel('Fator de potência'); ylabel('Perdas estimadas (MW)');
title('Sensibilidade das perdas ao fator de potência');
exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','sensibilidade-fp.png')); close(fig);
fprintf('Grafico 5/6 salvo: sensibilidade-fp.png\n');

spanCases = [200 250 300 350 400 450];
sagSensitivity = zeros(size(spanCases));
for k = 1:numel(spanCases)
    sagSensitivity(k) = span_state(p,spanCases(k),p.conductor_temperature_limit_c,0);
end
fig = figure('Visible','off');
plot(spanCases,sagSensitivity,'o-','LineWidth',1.2); grid on;
xlabel('Vão (m)'); ylabel('Flecha vertical (m)');
title('Sensibilidade mecânica ao comprimento do vão');
exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','sensibilidade-vaos.png')); close(fig);
fprintf('Grafico 6/6 salvo: sensibilidade-vaos.png\n');
end

% Summary values are screening results, not an engineering approval.
minAmpacity = min(ampacityBundle);
minMargin = min(thermalMargin);
minClearance = min(mechClearance);
clearanceStatus = "PASS_SCREEN";
if minClearance < p.design_ground_clearance_m
    clearanceStatus = "BELOW_ILLUSTRATIVE_CRITERION";
end
overload = any(Imax>ampacityBundle);
R = struct('eletrico',electrical,'mecanico',mechanical,'estruturas',structures, ...
    'ampacidade',thermal,'GMD_m',GMD,'GMR_feixe_m',GMRbundle, ...
    'ampacidade_A',minAmpacity,'Imax_A',Imax,'overload',overload, ...
    'margem_termica_minima_percentual',minMargin, ...
    'clearance_minimo_m',minClearance,'status_clearance',clearanceStatus);
fid = fopen(fullfile(projectRoot,'resultados','relatorios','resumo-resultados.md'),'w');
fprintf(fid,['# Resumo de resultados P24\n\n' ...
    'Modelo positivo-sequencia pi para 30 km e feixe duplo: GMD %.3f m; GMR equivalente %.4f m. ' ...
    'Foram calculados %d pares de carga e fator de potencia. Corrente maxima: %.2f A.\n\n' ...
    'Condutor do estudo: %s; dois subconductores por fase; afastamento %.2f m. ' ...
    'Corrente de catalogo: %.0f A por subconductor, sob as condicoes do fabricante.\n\n' ...
    'Triagem termica simplificada: %d pares ambiente/vento; ampacidade minima %.2f A; ' ...
    'margem minima %.2f%%; status %s.\n\n' ...
    'Analise mecanica parabolica: %d vaos em %d combinacoes temperatura/vento; clearance minimo ' ...
    'sintetico %.2f m versus criterio ilustrativo %.2f m (%s). Coordenadas locais ficticias, ' ...
    'origem na SE A; azimutes e cotas sinteticos.\n\n' ...
    'O modelo termico usa conveccao simplificada e radiacao/sol assumidos; nao e implementacao ' ...
    'certificada da IEEE 738. Nao foram calculadas sequencia zero, curto-circuito da rede, ' ...
    'estrutura/fundacoes ou coordenacao de isolamento. Perfil, clima e clearance nao sao dados ' ...
    'de campo nem demonstracao normativa.\n\n' ...
    'Projeto academico e conceitual. Nao deve ser utilizado para fabricacao, instalacao ou ' ...
    'execucao de servicos sem revisao, dimensionamento e responsabilidade de profissional ' ...
    'legalmente habilitado.\n'], ...
    GMD,GMRbundle,nElectrical,Imax,char(p.conductor_name),nSub,bundleSpacing,p.rated_current_a, ...
    nThermal,minAmpacity,minMargin,char(ternary(overload,'EXCEEDS_SCREEN','PASS_SCREEN')), ...
    height(mechanical),numel(tempGrid),minClearance,p.design_ground_clearance_m,char(clearanceStatus));
fclose(fid);
end

function [sagVertical,sagResultant,horizontalTension,supportTension] = span_state(p,span,tempC,wind)
g = 9.80665;
wv = p.conductor_mass_kg_m*g;
windLoad = 0.5*p.air_density_kg_m3*p.drag_coefficient*p.conductor_diameter_m*wind^2;
we = hypot(wv,windLoad);
EA = p.conductor_ea_n;
alpha = p.conductor_alpha_per_c;
H0 = p.reference_horizontal_tension_n;
T0 = p.reference_temperature_c;
f0 = wv*span^2/(8*H0);
arc0 = span+8*f0^2/(3*span);
target = arc0/(1+H0/EA)*(1+alpha*(tempC-T0));
compatibility = @(h) (span+8*(we*span^2/(8*h))^2/(3*span))/(1+h/EA)-target;
H = fzero(compatibility,[1000 500000]);
sagVertical = wv*span^2/(8*H);
sagResultant = we*span^2/(8*H);
horizontalTension = H;
supportTension = hypot(H,we*span/2);
end

function value = ternary(condition,a,b)
if condition
    value = a;
else
    value = b;
end
end
