# ComfyUI-Upscaler-Filename

A small utility custom node for ComfyUI that loads an upscale model and automatically generates clean filename prefixes based on the selected upscaler name.

It is useful when testing multiple upscalers because saved images and videos can be named after the model used, avoiding confusion between outputs.

## Node

**Upscale Model Loader with Filename**

The node behaves like an upscale model loader, but also outputs strings that can be connected to filename fields.

### Inputs

| Input | Description |
|---|---|
| `model_name` | Upscale model from `models/upscale_models` |
| `image_base` | Base output prefix for images |
| `video_base` | Base output prefix for videos |

### Outputs

| Output | Description |
|---|---|
| `upscale_model` | Connect to `ImageUpscaleWithModel` |
| `model_name_clean` | Sanitized model filename without extension |
| `image_filename_prefix` | Prefix for `Save Image` |
| `video_filename_prefix` | Prefix for `VHS Video Combine` or compatible video save nodes |

Example:

```text
RealESRGAN_x4plus.pth
```

becomes:

```text
RealESRGAN_x4plus
UpscalerFilename/Image_RealESRGAN_x4plus
UpscalerFilename/Video_RealESRGAN_x4plus
```

## Installation

### Manual install

1. Download this repository as a ZIP.
2. Extract it into your ComfyUI custom nodes folder:

```text
ComfyUI/custom_nodes/ComfyUI-Upscaler-Filename/
```

3. Restart ComfyUI.

### Git install

From your ComfyUI `custom_nodes` folder:

```bash
git clone https://github.com/giusparsifal/ComfyUI-Upscaler-Filename.git
```

Then restart ComfyUI.

## Usage

1. Add **Upscale Model Loader with Filename**.
2. Choose your upscale model.
3. Connect `upscale_model` to `ImageUpscaleWithModel`.
4. Convert the `filename_prefix` widget of `Save Image` or `VHS Video Combine` to an input.
5. Connect:
   - `image_filename_prefix` to `Save Image / filename_prefix`
   - `video_filename_prefix` to `VHS Video Combine / filename_prefix`

Now, when you change the selected upscaler, the output filename prefix changes automatically.

## Notes

- The node sanitizes model names so they are safe for filenames.
- It removes the model extension, such as `.pth` or `.safetensors`.
- It preserves folder-style prefixes, for example `UpscalerFilename/Image`.
- No external dependencies are required beyond ComfyUI's normal upscale model dependencies.

## Example workflow

See [`example_workflows/upscaler_filename_example.json`](example_workflows/upscaler_filename_example.json).

## License

MIT License. See [`LICENSE`](LICENSE).
