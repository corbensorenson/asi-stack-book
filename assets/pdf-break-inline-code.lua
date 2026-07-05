-- Make long inline code/path tokens breakable in reader-edition PDF output.
-- This filter is attached only to the generated PDF format.

local function contains_break_chars(text)
  return text:match("[/%._:#?&=-]") ~= nil
end

local function contains_space(text)
  return text:match("%s") ~= nil
end

local function should_wrap(text)
  return FORMAT:match("latex")
    and #text >= 28
    and not contains_space(text)
    and contains_break_chars(text)
end

local function path_literal(text)
  for _, delimiter in ipairs({ "|", "!", "+", ";", "," }) do
    if not text:find(delimiter, 1, true) then
      return "\\path" .. delimiter .. text .. delimiter
    end
  end
  return "\\nolinkurl{" .. text:gsub("}", "\\}") .. "}"
end

function Code(code)
  if should_wrap(code.text) then
    return pandoc.RawInline("latex", path_literal(code.text))
  end
end
