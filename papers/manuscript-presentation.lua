-- Resolve legacy manuscript contents against rendered headings in the same
-- version. The exact Markdown download is outside this display filter.
local function slug(text)
  return text:lower():gsub('[^%w%s_%-]', ''):gsub('%s', '-')
end

function Pandoc(doc)
  local ids, headings = {}, {}
  for index, block in ipairs(doc.blocks) do
    pandoc.Blocks({block}):walk({
      Header = function(header)
        local key = slug(pandoc.utils.stringify(header.content))
        ids[header.identifier] = true
        headings[#headings + 1] = {position = index, key = key, identifier = header.identifier}
      end,
      Div = function(div) ids[div.identifier] = true end,
      Span = function(span) ids[span.identifier] = true end,
    })
  end

  local function resolve(fragment, position)
    -- In source collections with several revisions, the nearest heading
    -- following the contents block belongs to the local revision.
    for _, item in ipairs(headings) do
      if item.position > position and item.key == fragment then return item.identifier end
    end
    local match
    for _, item in ipairs(headings) do
      if item.key == fragment then
        if match then return nil end
        match = item.identifier
      end
    end
    return match
  end

  local blocks = pandoc.Blocks({})
  for index, block in ipairs(doc.blocks) do
    blocks:extend(pandoc.Blocks({block}):walk({
      Link = function(link)
        local fragment = link.target:match('^#(.+)$')
        if not fragment or ids[fragment] then return end
        local target = resolve(fragment, index)
        if not target then
          -- Some versions changed the numbering or added a parenthetical
          -- heading subtitle. Match the heading text within this revision.
          local text = slug(pandoc.utils.stringify(link.content))
          for _, item in ipairs(headings) do
            local title = item.key:gsub('^%d+%-', '')
            if item.position > index and (title == text or title:sub(1, #text + 1) == text .. '-') then
              target = item.identifier
              break
            end
          end
        end
        if target then
          link.target = '#' .. target
          return link
        end
        -- An absent heading supplies no navigable destination.
        local content = pandoc.List(link.content)
        content:extend({pandoc.Space(), pandoc.Emph{pandoc.Str("(section unavailable)")}})
        return content
      end,
      Table = function(table)
        return pandoc.Div({table}, pandoc.Attr('', {'paper-table'}, {role = 'region', ['aria-label'] = 'Manuscript table', tabindex = '0'}))
      end
    }))
  end
  doc.blocks = blocks
  return doc
end
