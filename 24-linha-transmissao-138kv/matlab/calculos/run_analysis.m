function R=run_analysis
here=fileparts(mfilename('fullpath')); projectRoot=fileparts(fileparts(here)); addpath(fullfile(projectRoot,'matlab','funcoes'));
p=read_project_parameters(fullfile(projectRoot,'dados','parametros.csv')); f=p.frequency_hz; L=p.length_km*1000; Vll=p.voltage_kv*1000;
spacing=[p.phase_spacing_m_1 p.phase_spacing_m_2 p.phase_spacing_m_3]; gmd=prod([spacing(2)-spacing(1),spacing(3)-spacing(2),spacing(3)-spacing(1)])^(1/3);
GMR=p.conductor_gmr_m; radius=p.conductor_diameter_m/2; Lpkm=2e-4*log(gmd/GMR); Cpm=2*pi*8.8541878128e-12/log(gmd/radius);
R20=p.conductor_r20_ohm_km; alphaR=p.resistance_alpha_per_c; Tcond=[20 45 75]; loads=[p.load_active_mw_1 p.load_active_mw_2 p.load_active_mw_3]; pfs=[p.load_power_factor_1 p.load_power_factor_2 p.load_power_factor_3];
N=numel(loads); Psend=zeros(N,1); Ploss=zeros(N,1); Vs=zeros(N,1); reg=zeros(N,1); Irms=zeros(N,1); Srecv=zeros(N,1);
for k=1:N
 Rkm=R20*(1+alphaR*(Tcond(k)-20)); Z=(Rkm+1i*2*pi*f*Lpkm)*p.length_km; Y=1i*2*pi*f*Cpm*L;
 A=1+Y*Z/2; B=Z*(1+Y*Z/4); C=Y*(1+Y*Z/4); D=A;
 Precv=loads(k)*1e6; Qrecv=Precv*tan(acos(pfs(k))); Vr=Vll/sqrt(3); Ir=conj((Precv+1i*Qrecv)/(3*Vr)); Vsend=A*Vr+B*Ir; Isend=C*Vr+D*Ir;
 Vs(k)=sqrt(3)*abs(Vsend)/1000; reg(k)=100*(Vs(k)-p.voltage_kv)/p.voltage_kv; Irms(k)=abs(Ir); Srecv(k)=hypot(Precv,Qrecv)/1e6; Psend(k)=3*real(Vsend*conj(Isend))/1e6; Ploss(k)=Psend(k)-loads(k);
end
elect=table(loads(:),pfs(:),Srecv,Irms,Vs,reg,Psend,Ploss,'VariableNames',{'P_MW','fp','S_MVA','I_recebimento_A','V_envio_LL_kV','regulacao_percentual','P_envio_MW','perdas_MW'}); writetable(elect,fullfile(projectRoot,'resultados','tabelas','resultados-eletricos.csv'));
span=p.span_m; wv=p.conductor_mass_kg_m*9.80665; EA=p.conductor_ea_n; alpha=p.conductor_alpha_per_c; h0=p.reference_horizontal_tension_n; T0=p.reference_temperature_c;
temps=[20 45 75]; winds=[0 15 25]; M=numel(temps); sag=zeros(M,1); H=zeros(M,1); Tsupport=zeros(M,1); clearance=zeros(M,1);
for k=1:M
 ww=0.5*p.air_density_kg_m3*p.drag_coefficient*p.conductor_diameter_m*winds(k)^2; we=hypot(wv,ww); f0=wv*span^2/(8*h0); arc0=span+8*f0^2/(3*span);
 target=arc0/(1+h0/EA)*(1+alpha*(temps(k)-T0)); fun=@(h)(span+8*(we*span^2/(8*h))^2/(3*span))/(1+h/EA)-target;
 hh=fzero(fun,[1000 500000]); H(k)=hh; sag(k)=wv*span^2/(8*hh); Tsupport(k)=hypot(hh,we*span/2); clearance(k)=p.mean_conductor_height_m-sag(k);
end
mech=table(temps(:),winds(:),H/1000,sag,clearance,Tsupport/1000,'VariableNames',{'temperatura_C','vento_m_s','tracao_horizontal_kN','flecha_vertical_m','altura_livre_m','tracao_suporte_kN'}); writetable(mech,fullfile(projectRoot,'resultados','tabelas','resultados-mecanicos.csv'));
km=(0:2:p.length_km)'; elev=[p.route_elevation_m_1 p.route_elevation_m_2 p.route_elevation_m_3 p.route_elevation_m_4 p.route_elevation_m_5 p.route_elevation_m_6 p.route_elevation_m_7 p.route_elevation_m_8 p.route_elevation_m_9 p.route_elevation_m_10 p.route_elevation_m_11 p.route_elevation_m_12 p.route_elevation_m_13 p.route_elevation_m_14 p.route_elevation_m_15 p.route_elevation_m_16]'; nspan=round(p.length_km*1000/p.span_m);
structures=table((0:nspan)',(0:nspan)'*p.span_m/1000,interp1(km,elev,(0:nspan)'*p.span_m/1000,'linear','extrap'),repmat(p.span_m,nspan+1,1),'VariableNames',{'estrutura','km','elevacao_sintetica_m','vao_m'}); writetable(structures,fullfile(projectRoot,'resultados','tabelas','tabela-estruturas.csv'));
Tamb=45; Tc=75; D=p.conductor_diameter_m; Rm=R20*(1+alphaR*(Tc-20))/1000; qsolar=p.solar_absorptivity*p.solar_flux_w_m2*D; qconv=pi*D*p.thermal_h_w_m2_c*(Tc-Tamb); eps=0.5; sigma=5.670374419e-8; qrad=pi*D*eps*sigma*((Tc+273.15)^4-(Tamb+273.15)^4); Iamp=sqrt(max(0,(qconv+qrad-qsolar)/Rm)); Imax=max(Irms); margin=100*(Iamp-Imax)/Iamp; status="PASS"; if Imax>Iamp, status="EXCEEDS_THERMAL_ESTIMATE"; end
thermal=table(Tamb,Tc,Iamp,p.rated_current_a,Imax,margin,status,qsolar,qconv,qrad,'VariableNames',{'ambiente_C','condutor_C','ampacidade_estimada_A','corrente_referencia_A','corrente_maxima_casos_A','margem_percentual','status_termico','calor_solar_W_m','conveccao_W_m','radiacao_W_m'}); writetable(thermal,fullfile(projectRoot,'resultados','tabelas','ampacidade-estimada.csv'));
fig=figure('Visible','off'); tiledlayout(2,1); nexttile; plot(km,elev,'o-','LineWidth',1.2); grid on; xlabel('km'); ylabel('Cota sintética (m)'); title('Perfil longitudinal fictício'); nexttile; plot(temps,sag,'o-','LineWidth',1.2); grid on; xlabel('Temperatura (°C)'); ylabel('Flecha vertical (m)'); exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','perfil-flecha.png')); close(fig);
fig=figure('Visible','off'); plot(loads,Vs,'o-','LineWidth',1.2); grid on; xlabel('Carga recebida (MW)'); ylabel('Tensão de envio (kV LL)'); title('Fluxo por equivalente nominal π'); exportgraphics(fig,fullfile(projectRoot,'resultados','graficos','fluxo-carga.png')); close(fig);
R=struct('eletrico',elect,'mecanico',mech,'estruturas',structures,'ampacidade',thermal,'GMD_m',gmd,'ampacidade_A',Iamp,'Imax_A',Imax,'overload',Imax>Iamp);
fid=fopen(fullfile(projectRoot,'resultados','relatorios','resumo-resultados.md'),'w');
fprintf(fid,['# Resumo de resultados P24\n\nFluxo máximo entre os cenários: %.2f A. Ampacidade estimada a %.0f °C de ambiente e %.0f °C de condutor: %.2f A. Margem: %.2f%%. Status: %s.\n\nO status compara somente as hipóteses cadastradas em portfolio.toml; margem negativa pede rever condutor, corrente de projeto e condições térmicas. A estimativa não representa seleção comercial nem dimensionamento executivo.\n\nProjeto acadêmico e conceitual. Não deve ser utilizado para fabricação, instalação ou execução de serviços sem revisão, dimensionamento e responsabilidade de profissional legalmente habilitado.\n'],Imax,Tamb,Tc,Iamp,margin,char(status));
fclose(fid);
end
