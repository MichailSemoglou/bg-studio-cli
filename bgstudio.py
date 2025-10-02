#!/usr/bin/env python3
"""
BG Studio CLI

A Python script for intelligent background removal from images using the rembg library
with advanced masking controls and post-processing techniques.

Author: Michail Semoglou
License: MIT
Version: 1.0.0
Repository: https://github.com/MichailSemoglou/bg-studio-cli

Requirements:
    - rembg
    - pillow
    - numpy
    - onnxruntime
"""

from rembg import remove, new_session
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from io import BytesIO
import argparse
import sys
import os

__version__ = "1.0.0"
__author__ = "Michail Semoglou"
__license__ = "MIT"

def enhanced_background_removal(input_path, output_path, model='u2net', apply_postprocessing=True):
    """
    Enhanced background removal with better masking control
    
    Args:
        input_path: Path to input image
        output_path: Path to save output image
        model: Model to use ('u2net', 'u2net_human_seg', 'u2netp', 'isnet-general-use', 'silueta')
        apply_postprocessing: Whether to apply post-processing for better results
    """
    
    with open(input_path, 'rb') as f:
        input_data = f.read()
    
    session = new_session(model)
    output_data = remove(input_data, session=session)
    
    if apply_postprocessing:
        input_img = Image.open(BytesIO(input_data))
        output_img = Image.open(BytesIO(output_data))
        enhanced_img = post_process_mask(input_img, output_img)
        enhanced_img.save(output_path)
        return enhanced_img
    else:
        with open(output_path, 'wb') as f:
            f.write(output_data)
        return Image.open(BytesIO(output_data))

def post_process_mask(original_img, masked_img):
    """Apply post-processing techniques to improve mask quality"""
    if masked_img.mode != 'RGBA':
        masked_img = masked_img.convert('RGBA')
    
    alpha = masked_img.split()[-1]
    alpha_np = np.array(alpha)
    alpha_pil = Image.fromarray(alpha_np)
    
    alpha_filtered = alpha_pil.filter(ImageFilter.MedianFilter(size=3))
    alpha_smooth = alpha_filtered.filter(ImageFilter.GaussianBlur(radius=0.5))
    
    enhancer = ImageEnhance.Contrast(alpha_smooth)
    alpha_enhanced = enhancer.enhance(1.2)
    
    rgb_channels = masked_img.split()[:3]
    enhanced_img = Image.merge('RGBA', rgb_channels + (alpha_enhanced,))
    
    return enhanced_img

def create_custom_background(img, background_color=(255, 255, 255, 255)):
    """Replace transparent background with a custom color"""
    background = Image.new('RGBA', img.size, background_color)
    result = Image.alpha_composite(background, img)
    return result

def blend_edges(img, blur_radius=2):
    """Blend the edges of the mask for more natural results"""
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    alpha = img.split()[-1]
    blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    rgb_channels = img.split()[:3]
    blended_img = Image.merge('RGBA', rgb_channels + (blurred_alpha,))
    
    return blended_img

def parse_background_color(color_str):
    """Parse background color from string to RGBA tuple"""
    if color_str.lower() == 'transparent':
        return None
    elif color_str.lower() == 'white':
        return (255, 255, 255, 255)
    elif color_str.lower() == 'black':
        return (0, 0, 0, 255)
    elif color_str.lower() == 'red':
        return (255, 0, 0, 255)
    elif color_str.lower() == 'green':
        return (0, 255, 0, 255)
    elif color_str.lower() == 'blue':
        return (0, 0, 255, 255)
    elif color_str.startswith('#'):
        hex_color = color_str.lstrip('#')
        if len(hex_color) == 6:
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return (r, g, b, 255)
    elif ',' in color_str:
        values = [int(x.strip()) for x in color_str.split(',')]
        if len(values) == 3:
            return tuple(values + [255])
        elif len(values) == 4:
            return tuple(values)
    
    raise ValueError(f"Invalid color format: {color_str}")

def main():
    parser = argparse.ArgumentParser(
        description=f"BG Studio CLI v{__version__}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.jpg                           # Basic usage with defaults
  %(prog)s input.jpg -o output.png             # Specify output file
  %(prog)s input.jpg -m u2net_human_seg        # Use human-optimized model
  %(prog)s input.jpg -b white                  # White background instead of transparent
  %(prog)s input.jpg -b "#FF0000"              # Red background (hex color)
  %(prog)s input.jpg -b "255,0,0"              # Red background (RGB)
  %(prog)s input.jpg --blur 3                  # Apply edge blending
  %(prog)s input.jpg --no-postprocess          # Skip post-processing
  %(prog)s input.jpg --no-show                 # Don't display result

For more information, visit: https://github.com/MichailSemoglou/bg-studio-cli
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input image file path')
    parser.add_argument('-o', '--output', 
                       help='Output image file path (default: adds _nobg to input filename)')
    
    parser.add_argument('-m', '--model', 
                       choices=['u2net', 'u2net_human_seg', 'u2netp', 'isnet-general-use', 'silueta'],
                       default='u2net',
                       help='AI model to use (default: u2net)')
    
    parser.add_argument('-b', '--background',
                       default='transparent',
                       help='Background color: transparent, white, black, red, green, blue, #RRGGBB, or R,G,B')
    
    parser.add_argument('--blur', type=float, default=0,
                       help='Apply edge blending with specified blur radius (0 = no blending)')
    
    parser.add_argument('--no-postprocess', action='store_true',
                       help='Skip post-processing (faster but lower quality)')
    
    parser.add_argument('--no-show', action='store_true',
                       help='Don\'t display the result image')
    
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed processing information')
    
    parser.add_argument('--list-models', action='store_true',
                       help='List available models and exit')
    
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    if args.list_models:
        print("Available AI Models:")
        print("  u2net             - General purpose (default)")
        print("  u2net_human_seg   - Optimized for humans/portraits")
        print("  u2netp            - Lighter, faster version of u2net")
        print("  isnet-general-use - High accuracy general model")
        print("  silueta           - Good for objects with clear silhouettes")
        print("\nBackground Options:")
        print("  transparent       - Keep transparent background (PNG)")
        print("  white             - White background")
        print("  black             - Black background")
        print("  red, green, blue  - Solid color backgrounds")
        print("  #RRGGBB           - Custom hex color (e.g., #FF5733)")
        print("  R,G,B             - Custom RGB color (e.g., 255,87,51)")
        sys.exit(0)
    
    if args.input is None:
        print("Error: Input image file path is required.")
        parser.print_help()
        sys.exit(1)
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
    
    if args.output is None:
        input_name, input_ext = os.path.splitext(args.input)
        if args.background == 'transparent':
            args.output = f"{input_name}_nobg.png"
        else:
            args.output = f"{input_name}_nobg.jpg"
    
    try:
        background_color = parse_background_color(args.background)
    except ValueError as e:
        print(f"Error: {e}")
        print("Use --help for color format examples.")
        sys.exit(1)
    
    if args.verbose:
        print(f"Input: {args.input}")
        print(f"Output: {args.output}")
        print(f"Model: {args.model}")
        print(f"Background: {args.background}")
        if args.blur > 0:
            print(f"Edge blur: {args.blur}")
        print(f"Post-processing: {'enabled' if not args.no_postprocess else 'disabled'}")
        print()
    
    try:
        if args.verbose:
            print(f"Processing with {args.model} model...")
        
        result_img = enhanced_background_removal(
            args.input, 
            args.output, 
            model=args.model,
            apply_postprocessing=not args.no_postprocess
        )
        
        if args.blur > 0:
            if args.verbose:
                print(f"Applying edge blending (blur radius: {args.blur})...")
            result_img = blend_edges(result_img, blur_radius=args.blur)
        
        if background_color is not None:
            if args.verbose:
                print(f"Applying background color...")
            result_img = create_custom_background(result_img, background_color)
            result_img.save(args.output)
        
        if not args.no_show:
            result_img.show()
        
        print(f"✓ Background removed successfully!")
        print(f"✓ Result saved to: {args.output}")
        
    except Exception as e:
        print(f"Error processing image: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()