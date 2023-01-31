-- Copyright (C) 2023 Boba Birds Developers
--
-- Permission is hereby granted, free of charge, to any person obtaining a
-- copy of this software and associated documentation files (the "Software"),
-- to deal in the Software without restriction, including without limitation
-- the rights to use, copy, modify, merge, publish, distribute, sublicense,
-- and/or sell copies of the Software, and to permit persons to whom the
-- Software is furnished to do so, subject to the following conditions:
--
-- The above copyright notice and this permission notice shall be included in
-- all copies or substantial portions of the Software.
--
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
-- OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
-- FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
-- AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
-- LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
-- FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
-- DEALINGS IN THE SOFTWARE.

local love = require("love")
---@type RTA
local RTA = require("RTA")
local argparse = require("argparse")
local JSON = require("JSON")
local mounter = require("mounter")

local function getDir(path)
	---@type string
	path = love.path.normalslashes(path)

	if path:find("/", 1, true) == nil then
		return "."
	end

	local rpath = path:reverse()
	return rpath:sub(rpath:find("/", 1, true) or 1):reverse()
end

function love.load(arg, uarg)
	local parser = argparse(love.arg.getLow(uarg), "Custom bb_rw packer.", "Confidential")
	parser:argument("input", "RTA format input file")
	parser:argument("output", "Output directory", ".", function(p) return love.path.endslash(love.path.normalslashes(p)) end, "?")
	parser:option("-a --algorithm", "Select algorithm", "grid"):choices({"tree", "grid"})
	parser:flag("-2 --po2", "Always extend atlas to Power-of-2")

	local status, args = parser:pparse(arg)
	if not status then
		io.stderr:write("Error: ", args, "\n")
		print(parser:get_help())
		return love.event.quit(1)
	end

	args.output = args.output or "./"

	local inputFile = assert(io.open(args.input, "rb"))
	assert(mounter.MountPhysFS(getDir(args.input), "input", false))

	print("Input: "..args.input)

	-- Parse RTA files
	local rtaData = {
		output = love.path.leaf(args.input),
		size = 1024,
		extrude = -1,
		currentExtrude = 10,
		prefix = "",
		startFiles = false,
		file = {},
	}
	local atlas = RTA.newDynamicSize(0, 0, 0, args.algorithm)
	atlas:setMaxSize(1024, 1024)
	atlas:setExtrude(10)

	local lineCount = 1

	local function ensureNoFiles(command)
		if rtaData.startFiles then
			error("Unexpected '"..command.."' files already processed at line "..lineCount)
		end
	end

	local function ensureNumber(command, data)
		local num = tonumber(data)

		if num == nil then
			error("Invalid number for command '"..command.."' at line "..lineCount)
		end

		return math.floor(num)
	end

	local function loadImage(path, soft)
		local status, file = pcall(love.image.newImageData, "input/"..path)
		if not status then
			if soft then
				return nil
			else
				error(file.." at line "..lineCount)
			end
		end

		return file
	end

	local function addFile(path, soft)
		local file = loadImage(path, soft)

		if file then
			print(string.format("image %s dimension %dx%d", path, file:getDimensions()))
			if file:getWidth() >= rtaData.size or file:getHeight() >= rtaData.size then
				error("Image '"..path.."' exceeded maximum atlas size "..rtaData.size.." at line "..lineCount)
			end

			local id = rtaData.prefix..path
			local infoData = {
				image = file,
				id = id
			}
			atlas:add(file, id)
			rtaData.file[#rtaData.file + 1] = infoData
		else
			print("Image '"..path.."' is not a valid image file")
		end
	end

	for line in inputFile:lines() do
		line = line:gsub("\r", ""):gsub("\n", "")

		if #line > 0 then
			---@type string
			local command, data = line:match("(%a+)%s+(.+)")

			if not command then
				error("Unexpected data at line "..lineCount)
			end
			command = command:lower()

			if command == "output" then
				ensureNoFiles(command)
				rtaData.output = data
			elseif command == "size" then
				ensureNoFiles(command)
				rtaData.size = ensureNumber(command, data)
				atlas:setMaxSize(rtaData.size, rtaData.size)
				if rtaData.extrude == -1 then
					rtaData.currentExtrude = math.ceil(math.log(rtaData.size, 2))
					atlas:setExtrude(rtaData.currentExtrude)
				end
			elseif command == "prefix" then
				ensureNoFiles(command)
				rtaData.prefix = love.path.endslash(data)
			elseif command == "extrude" then
				ensureNoFiles(command)

				if data == "auto" then
					rtaData.extrude = -1
				else
					rtaData.extrude = ensureNumber(command, data)
					if rtaData.extrude < -1 then
						error("'"..command.."' must be -1 or auto, 0 or greater, at line "..lineCount)
					end
				end

				if rtaData.extrude == -1 then
					rtaData.currentExtrude = math.ceil(math.log(rtaData.size, 2))
					atlas:setExtrude(rtaData.currentExtrude)
				else
					atlas:setExtrude(rtaData.extrude)
				end
			elseif command == "file" then
				if not rtaData.startFiles then
					rtaData.startFiles = true
				end

				addFile(data)
			elseif command == "folder" then
				if not rtaData.startFiles then
					rtaData.startFiles = true
				end

				local normalData = love.path.endslash(love.path.normalslashes(data))

				for _, list in ipairs(love.filesystem.getDirectoryItems("input/"..data)) do
					local actualPath = normalData..list

					if love.filesystem.getInfo("input/"..actualPath, "file") then
						addFile(actualPath, true)
					end
				end
			end
		end

		lineCount = lineCount + 1
	end

	local baked
	local SORTBY = "area"
	if rtaData.extrude == -1 then
		print("Determining best extrude. Initial guess is "..rtaData.currentExtrude)

		-- Determine best extrude
		while true do
			atlas:setExtrude(rtaData.currentExtrude)
			baked = select(2, atlas:bake(SORTBY))
			local extrude = math.ceil(math.log(math.max(baked:getDimensions()), 2))
			if rtaData.currentExtrude ~= extrude then
				print("Current extrude: "..rtaData.currentExtrude.."; new extrude: "..extrude)
				rtaData.currentExtrude = extrude
				baked:release()
			else
				print("Found best extrude: "..extrude)
				rtaData.extrude = extrude
				break
			end
		end
	else
		baked = select(2, atlas:hardBake(SORTBY))
	end

	if math.max(baked:getDimensions()) > rtaData.size then
		error(string.format("Resulting atlas exceeded permitted POT size %d, atlas is %dx%d", rtaData.size, baked:getDimensions()))
	end

	if args.po2 then
		print("Ensuring PO2")

		local newBaked = love.image.newImageData(rtaData.size, rtaData.size)
		newBaked:paste(baked, 0, 0, 0, 0, baked:getDimensions())
		baked:release()
		baked = newBaked
	end

	local png = args.output..rtaData.output..".png"
	print("Writing "..png)

	local pngData = baked:encode("png")
	local pngOut = assert(io.open(png, "wb"))
	pngOut:write(pngData:getString())
	pngOut:close()

	local jsonFileOut = args.output..rtaData.output..".json"
	print("Writing "..jsonFileOut)

	local jsonData = {}

	for _, v in ipairs(rtaData.file) do
		jsonData[v.id] = {atlas:getViewport(v.id)}
	end

	local jsonData = JSON:encode_pretty(jsonData, nil, {pretty=true, indent="\t"})
	local jsonOut = assert(io.open(jsonFileOut, "wb"))
	jsonOut:write(jsonData)
	jsonOut:close()

	return love.event.quit(0)
end
