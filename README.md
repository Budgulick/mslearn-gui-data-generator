# MS Learn GUI Data Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-green)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🎯 Overview

A professional GUI application for the MS Learn Training Data Generator, built with CustomTkinter for a modern, responsive interface. Extract high-quality training data from Microsoft Learn documentation with a user-friendly interface featuring real-time progress tracking, batch processing, and comprehensive error handling.

## ✨ Features

### Phase 1 (MVP) - Current
- ✅ URL management (add/remove/validate)
- ✅ Output folder selection
- ✅ Real-time progress tracking
- ✅ Processing control (Start/Stop)
- ✅ Status logging
- ✅ Settings persistence
- ✅ Error handling with retry options

### Phase 2 (Coming Soon)
- 📋 File import and drag-drop support
- 📊 Dual progress bars
- 🎨 Color-coded URL status indicators
- 🔄 Bulk operations
- 📈 Enhanced statistics

### Phase 3 (Planned)
- 🔍 URL preview with tooltips
- 📊 Analytics dashboard
- 🎯 Advanced configuration presets
- ⌨️ Keyboard shortcuts
- 📤 Export capabilities

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Budgulick/mslearn-gui-data-generator.git
cd mslearn-gui-data-generator
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## 📁 Project Structure

```
mslearn-gui-data-generator/
├── src/
│   ├── gui/                  # GUI components
│   │   ├── main_window.py    # Main application window
│   │   ├── components/       # UI components
│   │   └── utils/            # GUI utilities
│   ├── core/                 # Core functionality
│   │   └── mslearn_generator.py
│   └── config/               # Configuration
│       └── settings.py
├── tests/                    # Unit tests
├── docs/                     # Documentation
├── requirements.txt          # Dependencies
└── main.py                   # Entry point
```

## 🔧 Configuration

Settings are automatically saved in JSON format and include:
- Output directory
- Quality thresholds
- Processing delays
- Window geometry
- Recent URL lists

## 📊 Development Status

### Current Phase: 1.1 - Project Setup ✅
- [x] Repository setup
- [x] Project structure
- [x] Dependencies configuration
- [ ] Main window framework (Next)

### Milestones
- **v0.1.0**: Initial setup
- **v1.0.0**: MVP complete
- **v1.2.0**: Enhanced UX
- **v2.0.0**: Production ready

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) for the modern UI framework
- Microsoft Learn for providing quality documentation
- Context7 for code validation support

## 📞 Support

For issues or questions:
- Open an [Issue](https://github.com/Budgulick/mslearn-gui-data-generator/issues)
- Check the [Documentation](docs/)
- Review the [Development Plan](GUI_DEVELOPMENT_PLAN.md)

---

**Development Status**: 🚧 Active Development - Phase 1 MVP