function p = read_project_parameters(file)
% Read flattened parameter CSV exported from portfolio.toml.
opts = detectImportOptions(file, 'Delimiter', ',', 'Encoding', 'UTF-8');
opts = setvartype(opts, {'name','value','unit','source'}, 'string');
T = readtable(file, opts);
p = struct();
for k = 1:height(T)
    name = matlab.lang.makeValidName(char(T.name(k)));
    rawValue = strtrim(T.value(k));
    numericValue = str2double(rawValue);
    if ismissing(rawValue) || strlength(rawValue) == 0
        error('portfolio:MissingParameterValue', ...
            'Parameter "%s" has no value in %s.', name, file);
    elseif isnan(numericValue)
        p.(name) = rawValue;
    else
        p.(name) = numericValue;
    end
end
end
