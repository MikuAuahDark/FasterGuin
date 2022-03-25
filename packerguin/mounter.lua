-- Copyright (C) 2022 Boba Birds Developers
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

local ffi = require("ffi")

local PhysFS = ffi.os == "Windows" and ffi.load("love") or ffi.C

local mounter = {}

ffi.cdef[[
bool PHYSFS_mount(const char *newDir, const char *mountPoint, bool appendToPath);
bool PHYSFS_unmount(const char *newDir);
int PHYSFS_getLastErrorCode();
const char *PHYSFS_getErrorByCode(int code);
]]

local errorCodeLookup = setmetatable({}, {
	__index = function(errorCodeLookup, code)
		local err = PhysFS.PHYSFS_getErrorByCode(code)
		local value = "Unknown error"

		if err ~= nil then
			value = ffi.string(err)
		end

		rawset(errorCodeLookup, code, value)
		return value
	end
})

---@return string
local function getLastPhysFSErr()
	return errorCodeLookup[PhysFS.PHYSFS_getLastErrorCode()]
end

---@param newDir string
---@param mountPoint string
---@param appendToPath boolean
function mounter.MountPhysFS(newDir, mountPoint, appendToPath)
	if not PhysFS.PHYSFS_mount(newDir, mountPoint, appendToPath) then
		return nil, getLastPhysFSErr()
	end

	return true
end

return mounter
