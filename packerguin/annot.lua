---@class RTA
local RTA = {}

---@param width integer
---@param height integer
---@param padding integer
---@param extrude integer
---@param spacing integer
---@return RTA.Atlas
function RTA.newFixedSize(width, height, padding, extrude, spacing)
end

---@param padding integer
---@param extrude integer
---@param spacing integer
---@return RTA.Atlas
function RTA.newDynamicSize(padding, extrude, spacing)
end

---@class RTA.Atlas
local Atlas = {}

---@param imageData boolean
function Atlas:useImageData(imageData)
end

---@param width integer
---@param height integer
function Atlas:setMaxSize(width, height)
end

---@param image love.Image|love.ImageData
---@param bake boolean
function Atlas:add(image, id, bake, ...)
end

---@param bake boolean
function Atlas:remove(id, bake)
end

---@return nil, love.ImageData
function Atlas:bake()
end

---@return nil, love.ImageData
function Atlas:hardBake()
end

---@return integer x
---@return integer y
---@return integer w
---@return integer h
function Atlas:getViewport(id)
end

---@param padding integer
function Atlas:setPadding(padding)
end

---@param extrude integer
function Atlas:setExtrude(extrude)
end

return RTA
