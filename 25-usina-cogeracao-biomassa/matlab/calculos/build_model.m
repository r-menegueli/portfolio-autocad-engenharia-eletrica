function build_model
here=fileparts(mfilename('fullpath')); projectRoot=fileparts(fileparts(here)); addpath(fullfile(projectRoot,'matlab','funcoes'));
p=read_project_parameters(fullfile(projectRoot,'dados','parametros.csv')); mdl='modelo_cogeracao_dinamico'; if bdIsLoaded(mdl),close_system(mdl,0);end; new_system(mdl); load_system('simulink');
H=p.inertia_constant_s; D=p.damping_pu; R=p.governor_droop_pu; Tg=p.governor_time_constant_s; Ka=p.avr_gain; Ta=p.avr_time_constant_s; X=p.generator_transient_reactance_pu; f=p.frequency_hz;
pm0=p.generator_active_mw/p.generator_efficiency/p.generator_rating_mva; pe0=p.generator_active_mw/p.generator_rating_mva;
q0=p.generator_active_mw*tan(acos(p.generator_power_factor))/p.generator_rating_mva; e0=sqrt((X*pe0)^2+(1+X*q0)^2);
e0dev=e0-1; delta0=atan2(X*pe0,1+X*q0); ploss=pm0-pe0;
script=sprintf(['function [dx,y]=fcn(u,x)\n' ...
 'v=u(2); pref=u(1); vref=u(3);\n' ...
 'efd=min(1.25,max(0.7,1+x(4))); pe=efd*v/%.12g*sin(x(1));\n' ...
 'vt=v+0.02*(x(4)-%.12g); q=(efd*v*cos(x(1))-v*v)/%.12g;\n' ...
 'de=(%.12g+%.12g*(vref-vt)-x(4))/%.12g; if x(4)>=0.25 && de>0, de=0; elseif x(4)<=-0.3 && de<0, de=0; end\n' ...
 'dx=[2*pi*%.12g*x(2);(x(3)-pe-%.12g-%.12g*x(2))/(2*%.12g);(pref-x(3)-x(2)/%.12g)/%.12g;de];\n' ...
 'y=[x(1);x(2);x(3);pe;x(4);q;vt];\nend\n'],X,e0dev,X,e0dev,Ka,Ta,f,ploss,D,H,R,Tg);
add_block('simulink/Sources/From Workspace',[mdl '/Inputs'],'VariableName','u_ts','Position',[30 70 150 100]);
add_block('simulink/Continuous/Integrator',[mdl '/States'],'InitialCondition',sprintf('[%.12g;0;%.12g;%.12g]',delta0,pm0,e0dev),'Position',[240 145 280 195]);
fb=[mdl '/Machine_governor_AVR']; add_block('simulink/User-Defined Functions/MATLAB Function',fb,'Position',[365 75 530 185]); rt=sfroot; chart=rt.find('-isa','Stateflow.EMChart','Path',fb); chart.Script=script;
add_block('simulink/Sinks/To Workspace',[mdl '/Y_log'],'VariableName','y_log','SaveFormat','Timeseries','Position',[615 75 715 105]); add_block('simulink/Sinks/To Workspace',[mdl '/X_log'],'VariableName','x_log','SaveFormat','Timeseries','Position',[365 245 465 275]);
add_line(mdl,'Inputs/1','Machine_governor_AVR/1'); add_line(mdl,'States/1','Machine_governor_AVR/2'); add_line(mdl,'Machine_governor_AVR/1','States/1'); add_line(mdl,'Machine_governor_AVR/2','Y_log/1'); add_line(mdl,'States/1','X_log/1');
set_param(mdl,'Solver','ode45','StopTime','5','ReturnWorkspaceOutputs','on'); save_system(mdl,fullfile(projectRoot,'simulink','modelo_cogeracao_dinamico.slx')); close_system(mdl,0);
end
