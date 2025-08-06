# GUI Requirements for MS Learn Training Data Generator

## 🎯 Core Requirements

### **Technology Stack**

- **Python + Tkinter/CustomTkinter** - Leverage existing Python codebase with modern UI components

### **Essential Features**

1. **URL Management** - Allow adding as many URLs as wanted with easy management
2. **Output Folder Selection** - Browse and select custom output directory
3. **Dual Progress Tracking** - Two progress bars for comprehensive monitoring:
   - Current URL progress (individual processing status)
   - Overall process progress (batch completion status)

## 📋 URL Management Features

### **Core URL Operations**

- **Import URLs from file** - Load from .txt, .csv, or existing URL inventory files
- **Drag-and-drop support** - Drop URL files directly onto the application
- **URL validation** - Check if URLs are valid MS Learn links before processing (Priority: Phase 1)
- **Duplicate detection** - Highlight/remove duplicate URLs automatically
- **URL preview** - Show title/category detection before processing with tooltips
- **Bulk URL operations** - Select multiple URLs for remove/validate operations
- **Save/Load URL lists** - Save project configurations for reuse

## ⚙️ Processing Control

### **Process Management**

- **Start/Pause/Stop buttons** - Control processing mid-batch
- **Skip failed URLs** - Continue processing when one URL fails
- **Retry failed URLs** - Automatically retry or manual retry option with retry queue management
- **Error details panel** - Expandable section showing specific error messages and solutions
- **Processing speed control** - Adjust delay between requests (respect rate limiting)
- **Processing stage indicators** - Show current stage (fetching, parsing, validating, etc.)

## 📊 Real-time Feedback

### **Live Status Updates**

- **Live processing log** - Scrollable text area showing current status
- **Quality score display** - Show quality scores as URLs are processed
- **Success/failure counters** - Running tally of processed/failed URLs
- **Current URL display** - Show which URL is being processed
- **Estimated time remaining** - Based on current processing speed

## 📁 Output Management

### **Result Monitoring**

- **Output preview** - Quick preview of generated training data
- **Category breakdown** - Show how many items per category (AD, DNS, etc.)
- **File size tracking** - Monitor output file sizes
- **Auto-backup** - Backup existing files before overwriting
- **Processing reports export** - CSV/JSON reports with timing, success rates, quality scores
- **Failed URLs export** - Export failed URLs for later retry
- **Training data preview** - Preview generated content before final save

## 🎨 Suggested UI Layout

```UI Sample
┌─────────────────────────────────────────────────────────────┐
│ MS Learn Training Data Generator                            │
├─────────────────────────────────────────────────────────────┤
│ [URL Management Section]                                    │
│ ┌─ URLs to Process ─────────────────────────────────────┐   │
│ │ URL 1: https://learn.microsoft... [Remove] [Preview] │   │
│ │ URL 2: https://learn.microsoft... [Remove] [Preview] │   │
│ │ ...                                                   │   │
│ └───────────────────────────────────────────────────────┘   │
│ [Add URL] [Import File] [Clear All] [Validate All]         │
├─────────────────────────────────────────────────────────────┤
│ [Settings Section]                                          │
│ Output Folder: [E:\path\to\output...] [Browse]             │
│ Category Name: [DNS_Administration▼] Delay: [2▼] seconds    │
├─────────────────────────────────────────────────────────────┤
│ [Progress Section]                                          │
│ Overall Progress: [████████░░] 8/10 URLs (80%)             │
│ Current URL: [███████░░░] Content extraction (70%)        │
│ Status: Processing "DNS Overview" - Quality Score: 345.2   │
├─────────────────────────────────────────────────────────────┤
│ [Statistics Panel]                                          │
│ Processed: 8 | Failed: 1 | Success Rate: 88.9%            │
│ Estimated Time Remaining: 2m 15s                           │
├─────────────────────────────────────────────────────────────┤
│ [Processing Log - Scrollable]                               │
│ 16:45:23 - Processing URL 8/10                             │
│ 16:45:25 - Quality score: 345.2 - ACCEPTED                 │
│ 16:45:26 - Generated training item: "DNS Overview"         │
├─────────────────────────────────────────────────────────────┤
│ [Control Buttons]                                           │
│ [▶ Start Processing] [⏸ Pause] [⏹ Stop] [💾 Save Results]   │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Additional Nice-to-Have Features

### 🎯 Advanced Processing Options

- **Quality threshold slider** - Set minimum quality score to accept
- **Content length limits** - Set min/max character limits
- **Category filtering** - Only process specific categories
- **Resume capability** - Resume interrupted batch processing

### 📊 Results Analysis

- **Quality distribution chart** - Visual breakdown of quality scores
- **Category distribution** - Pie chart of content by category
- **Processing time analytics** - Show average time per URL
- **Export statistics** - Save processing reports

### 🔄 Integration Features

- **Export to fine-tuning formats** - Direct export for training pipelines
- **Batch file generation** - Create scripts for command-line processing
- **Configuration presets** - Save common settings combinations

## 🎯 Development Phases

### **Phase 1: Core GUI (MVP)**

1. URL list management (add/remove/clear/validate)
2. Output folder selection with browse dialog
3. Combined progress bar (overall process with current stage indicator)
4. Start/Stop processing functionality
5. Basic status log with scrollable text area
6. Settings persistence (output folder, basic configs)
7. Error handling with retry options

### **Phase 2: Enhanced UX**

1. Import URLs from file (.txt, .csv support) and drag-and-drop
2. Dual progress bars (overall + current URL)
3. Processing statistics and counters
4. Real-time quality score display
5. Pause/Resume functionality
6. Enhanced error handling UI with detailed error panel
7. URL status indicators with color coding
8. Bulk URL operations

### **Phase 3: Advanced Features**

1. URL preview capabilities with tooltips
2. Advanced settings and configuration presets
3. Results preview and analysis with charts
4. Advanced processing options and filters
5. Export capabilities (reports, failed URLs, batch scripts)
6. Keyboard shortcuts and accessibility features
7. Processing analytics and performance metrics

## 🔧 Technical Integration

### **Core Integration Points**

- **Existing codebase leverage** - Use `MSLearnTrainingDataGenerator` class as backend
- **Threading support** - GUI remains responsive during processing
- **Progress callbacks** - Backend provides progress updates to GUI
- **Error propagation** - Proper error handling from backend to UI
- **Configuration management** - Save/restore GUI settings and URL lists

### **Dependencies**

```python
# Required packages
pip install customtkinter  # Modern UI components
pip install tkinter        # Built-in with Python
# Existing dependencies from main script:
# requests, beautifulsoup4, lxml
```

### **Architecture Pattern**

- **Model-View-Controller (MVC)** approach
- **MSLearnTrainingDataGenerator** - Model (existing)
- **CustomTkinter GUI** - View (new)
- **GUI Controller** - Controller (new, handles UI logic)

---

## 🔧 Additional Technical Recommendations

### **Threading Architecture**
```python
# Suggested structure:
- Main GUI Thread (UI updates)
- Worker Thread (processing URLs)
- Progress Callback Queue (thread-safe updates)
```

### **Settings Persistence**
```python
# JSON config file structure:
{
  "default_output_dir": "path",
  "quality_threshold": 100,
  "delay_seconds": 2,
  "recent_url_lists": ["file1.txt", "file2.csv"],
  "window_size": [1200, 800],
  "recent_categories": ["DNS_Administration", "Active_Directory"]
}
```

### **Memory Management**
- Process URLs in chunks for large lists (500+ URLs)
- Clear processed data from memory after saving
- Monitor memory usage during batch operations

### **CustomTkinter Components**
- `CTkProgressBar` for modern progress indicators
- `CTkScrollableFrame` for URL list management
- `CTkTabview` for organizing settings/results/logs
- `CTkOptionMenu` for dropdowns and selections

### **Keyboard Shortcuts**
- **Ctrl+A**: Add URL
- **Ctrl+S**: Start processing
- **Ctrl+P**: Pause/Resume
- **F5**: Refresh/Validate all URLs
- **Ctrl+E**: Export results
- **Ctrl+O**: Open URL list file

### **URL Status Color Coding**
- 🟢 **Green**: Ready to process
- 🟡 **Yellow**: Currently processing
- 🔴 **Red**: Failed (with error details)
- ✅ **Blue**: Completed successfully
- ⚪ **Gray**: Skipped or invalid

### **Error Handling Strategy**
- **Network errors**: Automatic retry with exponential backoff
- **Content quality**: User choice to skip or adjust thresholds
- **Invalid URLs**: Highlight and offer correction suggestions
- **File permissions**: Clear error messages with solutions

**Priority Focus:** Start with Phase 1 MVP to get core functionality working, then iterate through enhanced features based on user feedback and needs.