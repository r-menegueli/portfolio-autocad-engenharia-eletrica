function p = read_project_parameters(file)
% Read flattened parameter CSV exported from portfolio.toml.
T = readtable(file, 'TextType','string');
p = struct();
for k = 1:height(T)
    name = matlab.lang.makeValidName(char(T.name(k)));
    if isnumeric(T.value)
        value = double(T.value(k));
    else
        value = str2double(string(T.value(k)));
    end
    if isnan(value)
        p.(name) = string(T.value(k));
    else
        p.(name) = value;
    end
end
end
