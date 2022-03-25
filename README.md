Faster Guin
=====

A texture packer utilizing (fork of) [Runtime-TextureAtlas](https://github.com/EngineerSmith/Runtime-TextureAtlas) using LÖVE and Python.

Requirements
-----

* LÖVE 11.x - to run `packerguin` folder.

* Python 3.10 - tu run `fasterguin` module. 3.9 works but there's [issue](https://bugs.python.org/issue42233) with their typing module.

* ImageMagick 7 - ImageMagick 6 is **not** supported!

* [ASTCEnc](https://github.com/ARM-software/astc-encoder) - ASTC encoder required to run `android` profile (see below).

* [EtcTool](https://github.com/google/etc2comp) - ETC2 encoder required to run `low` profile (see below).

Usage
-----

Please run `python -m fasterguin`.

Profiles
-----

List of possible profiles:

* `pc` (default) - Only re-encode image to PNG. Resulting texture has `.png` extension.

* `android` - Encodes image to ASTC texture. Resulting texture has `.astc.ktx` extension.

* `low` - Encodes image to ETC2 texture. Resulting texture has `.etc2.ktx` extension.

Input File Format
-----

The input file format is as follows:  
```
<command> <input> [option_1 <value>] [option_2 <value>] ... [option_n <value>]
```

In most cases, `<input>` is the input file in your raw assets directory.

List of commands:

### `copyd`

Copy directory **recursively** to the output path. `<input>` is the directory to copy.

### `copyf`

Copy file to the output path. `<input>` is the file to copy.

### `file`

Include image file as part of the assets. `<input>` is the image file.

Accepts [`dimension`](###dimension) and [`resize`](###resize) options.

### `folder`

Include directory containing images **non-recursively** as part of the asets. `<input>` is the directory.

Accepts [`destination`](###destination), [`dimension`](###dimension), and [`resize`](###resize) options.

### `output`

Set the output file for the `metadata.json` (`<input>` parameter). The metadata contains the all original
dimensions and resized non-PO2'd images included in the assets in that order. The key is the path to the
image with prefix.

```json
{
	"path/to/image.png": [original image w, original image h, resized image w, resized image h]
}
```

The default is `metadata.json`.

### `pack`

Run Packer Guin. `<input>` is the Packer Guin input file. See below for the file syntax.

Accepts [`algorithm`](###algorithm) option.

### `prefix`

Set the output asset prefix for the metadata. `<input>` is the desired prefix.

Options
-----

The command can accept one or more options.

List of options:

### `algorithm`

Set the packer algorithm for the [`pack`](###pack) command. Valid options are:

* `tree` - Use Tree node packing algorithm.

* `grid` - Use RTA's custom packing algorithm.

The default is `grid` if this option is absent.

### `destination`

Set output destination relative to the output assets directory.

### `dimension`

Set the assumed image dimensions. Valid values are:

* `<w>x<h>` - Assume it's exactly specified.

* `original` - Use the original image dimension as-is.

If this option is absent, the image dimension is set to the original image or the
resized image (if [`resize`](###resize) option is present).

### `resize`

Resize the input image. Valid values are:

* `<w>x<h>` - Resize exactly to specified dimensions.

* `x<h>` - Automatically compute the width based on the ratio with fixed height.

* `<w>x` - Automatically compute the height based on the ratio with fixed width.

* `<scale>%` - Scale by percentage.

If this option is absent, the image is not resized.

Packer Guin Input
-----

TODO

License
-----

MIT.
