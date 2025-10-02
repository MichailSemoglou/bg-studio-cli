# Changelog

All notable chan- Custom background colors (solid colors, hex codes, RGB values)

- Edge blending for natural-looking soft edges
- Automatic output file naming
- Support for PNG (transparency) and JPG (solid background) output
- Comprehensive documentation and exampleso this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Nothing yet

### Changed

- Nothing yet

### Fixed

- Nothing yet

## [1.0.0] - 2025-10-02

### Added

- Initial release of BG Studio CLI
- Support for 5 different AI models (u2net, u2net_human_seg, u2netp, isnet-general-use, silueta)
- Full command-line interface with extensive options
- Advanced post-processing with noise reduction and edge smoothing
- Custom background colors (solid colors, hex codes, RGB values)
- Edge blending for natural-looking soft edges
- Automatic output file naming
- Support for PNG (transparency) and JPG (solid background) output
- Comprehensive documentation and examples
- Python API for programmatic usage
- Verbose mode for detailed processing information
- Model listing and help commands
- Input validation and error handling

### Technical Features

- **CLI Arguments**: Complete argument parsing with help and validation
- **Background Processing**: Multiple background color formats support
- **Image Processing**: Advanced mask post-processing techniques
- **Error Handling**: Comprehensive error messages and exit codes
- **Code Quality**: PEP 8 compliant code with proper documentation
- **Cross-Platform**: Works on macOS, Windows, and Linux

### Models Supported

- `u2net`: General purpose background removal
- `u2net_human_seg`: Optimized for human subjects and portraits
- `u2netp`: Lightweight version for faster processing
- `isnet-general-use`: High accuracy general-purpose model
- `silueta`: Optimized for objects with clear silhouettes

### Background Options

- Transparent (PNG output)
- Named colors (white, black, red, green, blue)
- Hex color codes (#RRGGBB)
- RGB values (R,G,B)
- RGBA values (R,G,B,A)

### Command Line Options

- `-o, --output`: Specify output file path
- `-m, --model`: Choose AI model
- `-b, --background`: Set background color/type
- `--blur`: Apply edge blending
- `--no-postprocess`: Skip post-processing for speed
- `--no-show`: Don't display result image
- `-v, --verbose`: Show detailed processing info
- `--list-models`: List available models
- `--version`: Show version information

## [Future Releases]

### Planned Features

- [ ] Batch processing for multiple images
- [ ] GUI interface
- [ ] Video processing support
- [ ] Cloud processing integration
- [ ] Additional AI model support
- [ ] Performance optimizations
- [ ] Docker containerization
- [ ] Web API endpoint

---

## Version History Summary

- **v1.0.0**: Initial release with full CLI interface and 5 AI models
- **v0.x.x**: Development versions (not released)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
