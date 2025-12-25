# 📐 面積計算機 (Area Calculator)

A professional construction area and material calculator designed for construction professionals, contractors, and project managers to accurately calculate areas and optimize protective sheet (養生シート) material requirements.

## 🎯 Features

### 🏠 多室計算 (Multi-Room Calculator)
- Calculate floor, ceiling, and wall areas for multiple rooms
- Detailed breakdowns with real-time calculations
- Support for custom room dimensions

### 🏗️ 外壁足場養生 (Exterior Scaffolding Protection)
- Specialized calculator for exterior wall scaffolding protection covering
- Standard scaffolding unit dimensions support (1.829m × 0.9m × 1.725m)
- Horizontal strip calculation for side wall coverage

### 🛡️ スマート養生シート (Smart Protective Sheet Calculator)
- AI-powered optimization for protective sheet material requirements
- Cross-room material sharing to minimize waste
- Mixed roll size selection (1800mm and 3600mm rolls)
- Layer-aware calculations (0.1mm for walls/ceilings, 0.15mm for floors)

## 🔧 Technical Specifications

- **Roll Sizes:** 1800mm × 50m and 3600mm × 50m protective sheets
- **Coverage Calculations:** Includes 20% overlap factor for real-world application
- **Safety Margins:** Includes 0.6m additional material allowance for floor applications
- **Smart Optimization:** Advanced algorithms reduce material waste through intelligent allocation

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/[YOUR_USERNAME]/area-calculator.git
cd area-calculator
```

2. Install required dependencies:
```bash
pip install streamlit
```

3. Run the application:
```bash
streamlit run app.py
```

## 📋 Usage

1. **Multi-Room Calculator**: Add rooms with their dimensions (length, width, height)
2. **Scaffolding Calculator**: Enter building dimensions and scaffolding unit specifications
3. **Smart Calculator**: Import room data and select surfaces for optimized material calculation

## 🛠️ Dependencies

- Python 3.7+
- Streamlit
- Math (built-in)

## 💡 Use Cases

- Interior renovation projects with multiple rooms
- Exterior building protection during construction
- Scaffolding coverage planning for high-rise buildings
- Material procurement optimization for construction sites
- Cost estimation for protective sheet requirements

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions, please create an issue in this repository.
