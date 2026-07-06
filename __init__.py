"""
ComfyUI-Upscaler-Filename

A small ComfyUI custom node that loads an upscale model and also outputs
clean filename prefixes based on the selected upscaler name.
"""

from __future__ import annotations

import logging
import os
import re
from typing import Tuple

import comfy.utils
import folder_paths
from spandrel import ImageModelDescriptor, ModelLoader

# Match ComfyUI's upscale loader behavior for extra/non-commercial arches when available.
try:
    from spandrel import MAIN_REGISTRY
    from spandrel_extra_arches import EXTRA_REGISTRY

    MAIN_REGISTRY.add(*EXTRA_REGISTRY)
except Exception as exc:  # Optional dependency/path; ComfyUI can still load common models.
    logging.debug("Upscaler Filename: spandrel_extra_arches not loaded: %s", exc)


class UpscaleModelLoaderWithFilename:
    """Load an upscale model and create filename prefixes from its model name.

    Outputs:
        upscale_model: UPSCALE_MODEL, compatible with ImageUpscaleWithModel.
        model_name_clean: sanitized model filename without extension.
        image_filename_prefix: base path + sanitized model name for Save Image.
        video_filename_prefix: base path + sanitized model name for VHS Video Combine.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_name": (folder_paths.get_filename_list("upscale_models"),),
                "image_base": (
                    "STRING",
                    {
                        "default": "UpscalerFilename/Image",
                        "tooltip": "Base prefix for image outputs. The model name will be appended automatically.",
                    },
                ),
                "video_base": (
                    "STRING",
                    {
                        "default": "UpscalerFilename/Video",
                        "tooltip": "Base prefix for video outputs. The model name will be appended automatically.",
                    },
                ),
            }
        }

    RETURN_TYPES = ("UPSCALE_MODEL", "STRING", "STRING", "STRING")
    RETURN_NAMES = (
        "upscale_model",
        "model_name_clean",
        "image_filename_prefix",
        "video_filename_prefix",
    )
    FUNCTION = "load_model_with_filename"
    CATEGORY = "image/upscaling"
    DESCRIPTION = "Loads an upscale model and outputs filename prefixes based on the selected upscaler name."

    @staticmethod
    def _clean_model_name(model_name: str) -> str:
        """Return a filesystem-safe model name without extension."""
        name = os.path.splitext(os.path.basename(str(model_name)))[0]
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._-")
        return name or "upscaler"

    @staticmethod
    def _normalize_base(prefix: str, fallback: str) -> str:
        """Normalize an output prefix while preserving subfolders."""
        prefix = str(prefix or fallback).strip()
        prefix = prefix.replace("\\", "/")
        prefix = prefix.rstrip("_-/\\ ")
        return prefix or fallback

    @staticmethod
    def _load_upscale_model(model_name: str):
        """Standalone upscale model loading logic compatible with recent ComfyUI versions."""
        model_path = folder_paths.get_full_path_or_raise("upscale_models", model_name)
        state_dict = comfy.utils.load_torch_file(model_path, safe_load=True)

        # Compatibility for some checkpoints saved with a "module." prefix.
        if "module.layers.0.residual_group.blocks.0.norm1.weight" in state_dict:
            state_dict = comfy.utils.state_dict_prefix_replace(state_dict, {"module.": ""})

        model = ModelLoader().load_from_state_dict(state_dict).eval()
        if not isinstance(model, ImageModelDescriptor):
            raise ValueError("Upscale model must be a single-image model.")

        return model

    def load_model_with_filename(
        self,
        model_name: str,
        image_base: str,
        video_base: str,
    ) -> Tuple[object, str, str, str]:
        upscale_model = self._load_upscale_model(model_name)
        clean_name = self._clean_model_name(model_name)

        image_base = self._normalize_base(image_base, "UpscalerFilename/Image")
        video_base = self._normalize_base(video_base, "UpscalerFilename/Video")

        image_prefix = f"{image_base}_{clean_name}"
        video_prefix = f"{video_base}_{clean_name}"

        return upscale_model, clean_name, image_prefix, video_prefix


NODE_CLASS_MAPPINGS = {
    "UpscaleModelLoaderWithFilename": UpscaleModelLoaderWithFilename,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "UpscaleModelLoaderWithFilename": "Upscale Model Loader with Filename",
}
