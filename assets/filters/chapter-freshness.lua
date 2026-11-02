-- Chapter front matter owns declared revision events. Legacy literal table
-- dates are presentation inputs only and are replaced, never re-dated.
local function text(value)
  return value and pandoc.utils.stringify(value) or nil
end

-- Quarto 1.9 replaces global error() with a non-fatal logger. The Lua
-- assertion primitive still throws; guard failures must abort Pandoc.
local function reject(message)
  assert(false, message)
end

local function calendar_date(value, key)
  local y, m, d = (value or ''):match('^(%d%d%d%d)%-(%d%d)%-(%d%d)$')
  y, m, d = tonumber(y), tonumber(m), tonumber(d)
  local days = {31,28,31,30,31,30,31,31,30,31,30,31}
  if y and (y % 400 == 0 or (y % 4 == 0 and y % 100 ~= 0)) then days[2] = 29 end
  if not y or y < 1 or not m or m < 1 or m > 12 or not d or d < 1 or d > days[m] then
    reject(key .. ' requires a canonical calendar date')
  end
  if value > os.date("!%Y-%m-%d") then reject(key .. " cannot declare a future event") end
  return value
end

local function cell(value)
  return pandoc.Cell({pandoc.Plain({pandoc.Str(value)})})
end
local function row(label, value)
  return pandoc.Row({cell(label), cell(value)})
end

function Pandoc(doc)
  if not doc.meta.chapter_id then return doc end
  local revision = calendar_date(text(doc.meta.last_updated), 'last_updated')
  local review = text(doc.meta.source_reviewed_on)
  local scope = text(doc.meta.source_review_scope)
  if (review ~= nil) ~= (scope ~= nil) or (scope and not scope:match('%S')) then
    reject('source_reviewed_on and a bounded source_review_scope are required together')
  end
  if review then review = calendar_date(review, 'source_reviewed_on') end
  local in_status, sections, found, status_index = false, 0, 0, nil
  local metadata_table
  for index, block in ipairs(doc.blocks) do
    if block.t == 'Header' and block.level <= 2 then
      in_status = block.level == 2 and text(block.content) == 'Chapter status'
      if in_status then sections, status_index = sections + 1, index end
    elseif in_status and block.t == 'Table' then
      found, metadata_table = found + 1, block
    end
  end
  if sections ~= 1 or found > 1 then
    reject('chapter requires one Chapter status section with at most one metadata table')
  end
  if not metadata_table then
    -- Consolidated owners may use a prose-only status section. Generate just
    -- the date table; retain every original prose block in its original order.
    metadata_table = pandoc.read('| Field | Value |\n|---|---|\n| Chapter revision | placeholder |', 'markdown').blocks[1]
    doc.blocks:insert(status_index + 1, metadata_table)
  end
  if #metadata_table.colspecs ~= 2 then reject('chapter-status metadata table requires two columns') end
  for _, body in ipairs(metadata_table.bodies) do
    local kept = pandoc.List()
    for _, existing in ipairs(body.body) do
      local label = existing.cells[1] and text(existing.cells[1].contents)
      if label ~= 'Last updated' and label ~= 'Chapter revision' and
         label ~= 'Source review' and label ~= 'Source review scope' then
        kept:insert(existing)
      end
    end
    body.body = kept
  end
  local rows = metadata_table.bodies[1].body
  rows:insert(row('Chapter revision', revision))
  rows:insert(row('Source review', review or 'Not recorded in chapter metadata; see source records'))
  if scope then rows:insert(row('Source review scope', scope)) end
  return doc
end
