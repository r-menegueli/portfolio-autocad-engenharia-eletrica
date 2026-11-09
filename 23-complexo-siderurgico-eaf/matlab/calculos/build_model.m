function build_model
here=fileparts(mfilename('fullpath')); projectRoot=fileparts(fileparts(here));
addpath(fullfile(projectRoot,'matlab','funcoes'));
p=read_project_parameters(fullfile(projectRoot,'dados','parametros.csv'));
mdl='modelo_eaf_dinamico'; if bdIsLoaded(mdl), close_system(mdl,0); end
new_system(mdl); load_system('simulink');
qfilter=p.filter_total_mvar/p.main_transformer_mva; qmax=p.statcom_limit_mvar/p.main_transformer_mva;
zsrc=p.main_transformer_mva/p.source_short_circuit_mva;
xth=p.main_transformer_x_pu+zsrc; rth=p.main_transformer_r_pu;
pf=p.target_power_factor; tauv=p.bus_voltage_time_constant_s; tauq=p.statcom_time_constant_s;
script=sprintf(['function [dx,y]=fcn(u,x)\n' ...
 'p=u(1); q=u(2); en=u(3); vg=u(4); arc=u(5);\n' ...
 'qgrid=abs(p)*tan(acos(%.12g));\n' ...
 'qref=en*min(%.12g,max(-%.12g,q-qgrid-%.12g));\n' ...
 'qnet=q-%.12g-x(2);\n' ...
 'vref=vg-%.12g*p-%.12g*qnet+arc;\n' ...
 'dx=[(vref-x(1))/%.12g;(qref-x(2))/%.12g];\n' ...
 's=sqrt(p*p+qnet*qnet); pfout=abs(p)/max(s,1e-6);\n' ...
 'y=[x(1);x(2);qnet;pfout];\nend\n'],pf,qmax,qmax,qfilter,qfilter,rth,xth,tauv,tauq);
add_block('simulink/Sources/From Workspace',[mdl '/Inputs'],'VariableName','u_ts','Position',[30 70 150 100]);
add_block('simulink/Continuous/Integrator',[mdl '/States'],'InitialCondition','[1;0]','Position',[245 155 280 195]);
fb=[mdl '/Dynamic_equivalent']; add_block('simulink/User-Defined Functions/MATLAB Function',fb,'Position',[365 75 510 175]); rt=sfroot; chart=rt.find('-isa','Stateflow.EMChart','Path',fb); chart.Script=script;
add_block('simulink/Sinks/To Workspace',[mdl '/Y_log'],'VariableName','y_log','SaveFormat','Timeseries','Position',[600 75 700 105]);
add_block('simulink/Sinks/To Workspace',[mdl '/X_log'],'VariableName','x_log','SaveFormat','Timeseries','Position',[365 230 465 260]);
add_line(mdl,'Inputs/1','Dynamic_equivalent/1'); add_line(mdl,'States/1','Dynamic_equivalent/2');
add_line(mdl,'Dynamic_equivalent/1','States/1'); add_line(mdl,'Dynamic_equivalent/2','Y_log/1'); add_line(mdl,'States/1','X_log/1');
set_param(mdl,'Solver','ode45','StopTime','5','ReturnWorkspaceOutputs','on','SaveTime','off');
save_system(mdl,fullfile(projectRoot,'simulink','modelo_eaf_dinamico.slx')); close_system(mdl,0);
end
