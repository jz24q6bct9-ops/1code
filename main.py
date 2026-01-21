"""
Blender script to process frames from a directory.

Usage:
    blender --background --python main.py -- --frames_dir path --fps 30
"""

import sys
import argparse
from pathlib import Path


def parse_arguments():
    """
    Parse command-line arguments.
    
    When running with Blender, arguments after '--' are passed to the script.
    """
    # Find the separator '--' in sys.argv
    if '--' in sys.argv:
        # Get arguments after the '--' separator
        script_args = sys.argv[sys.argv.index('--') + 1:]
    else:
        # No separator found, use all arguments after script name
        script_args = sys.argv[1:]
    
    parser = argparse.ArgumentParser(
        description='Process frames in Blender',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        '--frames_dir',
        type=str,
        required=True,
        help='Directory containing frames to process'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=30,
        help='Frames per second (default: 30)'
    )
    
    args = parser.parse_args(script_args)
    return args


def process_frames(frames_dir, fps):
    """
    Process frames from the specified directory.
    
    Args:
        frames_dir: Path to directory containing frames
        fps: Frames per second for rendering
    """
    frames_path = Path(frames_dir)
    
    if not frames_path.exists():
        raise FileNotFoundError(f"Frames directory not found: {frames_dir}")
    
    if not frames_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {frames_dir}")
    
    print(f"Processing frames from: {frames_path.absolute()}")
    print(f"FPS: {fps}")
    
    # Import Blender API (only available when running within Blender)
    try:
        import bpy
        
        # Set render FPS
        bpy.context.scene.render.fps = fps
        print(f"Blender scene FPS set to: {fps}")
        
        # Get list of frame files
        frame_files = sorted([
            f for f in frames_path.iterdir()
            if f.is_file() and f.suffix.lower() in {'.png', '.jpg', '.jpeg', '.exr', '.tiff', '.tif'}
        ])
        
        if not frame_files:
            print(f"Warning: No image files found in {frames_dir}")
            return
        
        print(f"Found {len(frame_files)} frame files")
        
        # Process frames
        for idx, frame_file in enumerate(frame_files, start=1):
            print(f"Processing frame {idx}/{len(frame_files)}: {frame_file.name}")
            # Add custom processing logic here
            
        print("Frame processing complete!")
        
    except ImportError:
        print("Warning: Blender Python API (bpy) not available.")
        print("This script should be run with: blender --background --python main.py -- --frames_dir path --fps 30")
        print(f"\nDry run mode:")
        print(f"  Frames directory: {frames_path.absolute()}")
        print(f"  FPS: {fps}")
        
        # List available frames even without Blender
        frame_files = list(frames_path.glob('*.*'))
        if frame_files:
            print(f"  Found {len(frame_files)} files in directory")


def main():
    """Main entry point."""
    try:
        args = parse_arguments()
        process_frames(args.frames_dir, args.fps)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
