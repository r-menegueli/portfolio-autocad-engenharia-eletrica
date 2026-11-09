function R=run_analysis
here=fileparts(mfilename('fullpath')); projectRoot=fileparts(fileparts(here));
addpath(fullfile(projectRoot,'matlab','funcoes')); p=read_project_parameters(fullfile(projectRoot,'dados','parametros.csv'));
furnaceS=p.furnace_transformer_mva; furnaceP=furnaceS*p.furnace_power_factor;
furnaceQ=furnaceS*sin(acos(p.furnace_power_factor)); auxP=p.auxiliary_active_mw;
auxQ=auxP*tan(acos(p.auxiliary_power_factor)); P=furnaceP+auxP; Q=furnaceQ+auxQ;
Qtarget=P*tan(acos(p.target_power_factor)); Qstat=max(0,Q-p.filter_total_mvar-Qtarget);
Sraw=hypot(P,Q); Sgrid=hypot(P,Qtarget); Igrid=Sgrid*1e6/(sqrt(3)*p.grid_voltage_kv*1e3);
Ibus=Sgrid*1e6/(sqrt(3)*p.bus_voltage_kv*1e3); Ifurnace=p.furnace_transformer_mva*1e6/(sqrt(3)*p.furnace_secondary_voltage_kv*1e3);
base=p.main_transformer_mva; zsrc=base/p.source_short_circuit_mva; rth=p.main_transformer_r_pu; xth=p.main_transformer_x_pu+zsrc;
Scc=base/sqrt(rth^2+xth^2); Icc=Scc*1e6/(sqrt(3)*p.bus_voltage_kv*1e3);
thd=sqrt(sum([p.harmonic_current_pu_1 p.harmonic_current_pu_2 p.harmonic_current_pu_3 p.harmonic_current_pu_4].^2));
balance=table(P,Q,Sraw,P/Sraw,Qtarget,p.filter_total_mvar,Qstat,Sgrid,Igrid,Ibus,Ifurnace,'VariableNames',{'P_MW','Q_bruta_MVAr','S_bruta_MVA','fp_bruto','Q_rede_alvo_MVAr','Q_filtros_MVAr','Q_STATCOM_MVAr','S_PCC_MVA','I_PCC_A','I_B1_A','I_secundaria_A'});
writetable(balance,fullfile(projectRoot,'resultados','tabelas','balanco-cargas.csv'));
short=table(base,zsrc,rth,xth,Scc,Icc,'VariableNames',{'Base_MVA','X_fonte_pu','R_transformador_pu','X_total_pu','Scc_34k5_MVA','Icc_34k5_kA'}); short.Icc_34k5_kA=short.Icc_34k5_kA/1000;
writetable(short,fullfile(projectRoot,'resultados','tabelas','curto-circuito.csv'));
orders=[5;7;11;13]; amps=[p.harmonic_current_pu_1;p.harmonic_current_pu_2;p.harmonic_current_pu_3;p.harmonic_current_pu_4]; harm=table(orders,amps,100*amps,'VariableNames',{'ordem','Ih_pu','Ih_percentual_fundamental'});
harm.THDi_global_percentual=repmat(100*thd,height(harm),1); writetable(harm,fullfile(projectRoot,'resultados','tabelas','harmonicos.csv'));
build_model;
mdl='modelo_eaf_dinamico'; load_system(fullfile(projectRoot,'simulink',[mdl '.slx']));
t=(0:0.01:5)'; pload=(P/base)*ones(size(t)); qload=(Q/base)*ones(size(t)); qload(t>=1.2)=1.2*Q/base; qload(t>=3.2)=0.8*Q/base;
vgrid=ones(size(t)); arc=p.arc_fluctuation_pu*sin(2*pi*2*t);
assignin('base','u_ts',timeseries([pload qload zeros(size(t)) vgrid arc],t)); out0=sim(mdl,'StopTime','5','ReturnWorkspaceOutputs','on'); y0=out0.get('y_log');
assignin('base','u_ts',timeseries([pload qload ones(size(t)) vgrid arc],t)); out1=sim(mdl,'StopTime','5','ReturnWorkspaceOutputs','on'); y1=out1.get('y_log');
T0=timeseries_table(y0); T1=timeseries_table(y1); T0.scenario=repmat("sem_STATCOM",height(T0),1); T1.scenario=repmat("com_STATCOM",height(T1),1); dyn=[T0;T1];
writetable(dyn,fullfile(projectRoot,'resultados','tabelas','dinamica-tensao.csv'));
fig=figure('Visible','off'); tiledlayout(2,1); nexttile; plot(T0.time_s,T0.V_pu,T1.time_s,T1.V_pu,'LineWidth',1.2); grid on; ylabel('Tensão (pu)'); legend('sem STATCOM','com STATCOM','Location','best'); title('Resposta dinâmica conceitual da barra'); nexttile; plot(T1.time_s,T1.Qstat_pu*base,'LineWidth',1.2); grid on; ylabel('Q STATCOM (MVAr)'); xlabel('Tempo (s)'); exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','resposta-dinamica.png')); close(fig);
fig=figure('Visible','off'); bar([P Qtarget p.filter_total_mvar Qstat]); xticklabels({'P total MW','Q PCC alvo MVAr','Filtros MVAr','STATCOM MVAr'}); grid on; title('Balanço de carga e compensação'); exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','balanco-compensacao.png')); close(fig);
R=struct('P_MW',P,'Q_bruta_MVAr',Q,'Q_STATCOM_MVAr',Qstat,'fp_bruto',P/Sraw,'I_PCC_A',Igrid,'Icc_34k5_kA',Icc/1000,'THDi_sintetico',thd,'dinamica',dyn);
end
function T=timeseries_table(ts)
d=squeeze(ts.Data); if size(d,1)~=numel(ts.Time) && size(d,2)==numel(ts.Time), d=d'; end
T=table(ts.Time,d(:,1),d(:,2),d(:,3),d(:,4),'VariableNames',{'time_s','V_pu','Qstat_pu','Qgrid_pu','fp_pu'});
end
