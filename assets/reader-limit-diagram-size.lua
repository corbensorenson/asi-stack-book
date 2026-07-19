-- Keep generated Mermaid figures inside printable PDF/DOCX geometry.
-- HTML and EPUB keep their responsive native handling.

local function is_stack_map(src)
  return src:match("asi%-is%-a%-stack%-not%-a%-model_files/.*/mermaid%-figure") ~= nil
end

local function is_policy_interface(src)
  return src:match("policy%-optimization%-and%-learning%-from%-feedback_files/.*/mermaid%-figure%-2") ~= nil
end

function Image(image)
  if FORMAT:match("latex") then
    if is_stack_map(image.src) then
      image.attributes.width = "100%"
      image.attributes.height = "7in"
      return image
    end
    if is_policy_interface(image.src) then
      image.attributes.width = "100%"
      image.attributes.height = "5.8in"
      return image
    end
  end
  if FORMAT:match("docx") and is_stack_map(image.src) then
    image.attributes.width = "6.2in"
    image.attributes.height = "7in"
    return image
  end
end
