# ZeroWriter for 7.5" Waveshare Display

## Overview

This is an adapted version of ZeroWriter for the **Waveshare 7.5" V2 e-Paper display** (800x480 resolution). The larger display provides significantly more writing space compared to the original 4.2" version.

## Display Specifications

- **Model**: Waveshare 7.5" V2 e-Paper
- **Resolution**: 800×480 pixels (vs 4.2" at 400×300)
- **Screen Size**: 2× wider, 1.6× taller than original
- **Driver**: `epd7in5_V2_fast.py` with optimized LUT tables for fast partial refresh

## Layout Improvements for 7.5" Display

### Comparison: 4.2" vs 7.5"

| Feature | 4.2" Display | 7.5" Display | Improvement |
|---------|--------------|--------------|-------------|
| **Resolution** | 400×300 | 800×480 | 2× width, 1.6× height |
| **Font Size** | 18pt | 24pt | +33% larger |
| **Characters per Line** | 32 | 64 | 2× more characters |
| **Visible Lines** | 12 | 16 | +33% more lines |
| **Line Spacing** | 22px | 28px | Proportional to font |
| **Total Visible Text** | ~384 chars | ~1024 chars | **2.67× more text** |

### Text Area Layout

```
┌─────────────────────────────────────────┐
│                                         │
│  Text Area (800×450px)                  │
│  - 16 lines of previous text            │
│  - 64 characters per line                │
│  - 24pt Courier Prime font               │
│                                         │
│                                         │
├─────────────────────────────────────────┤
│  Input Line (800×30px)              [1/5]│ ← Console messages
└─────────────────────────────────────────┘
```

## Files Included

- **`main_7in5.py`** - Main application adapted for 7.5" display
- **`keymaps.py`** - Keyboard mapping (with bug fixes)
- **`epd7in5_V2_fast.py`** - Fast refresh display driver (in `waveshare_epd/`)
- **`README_7IN5.md`** - This file

## Bug Fixes Applied

This adapted version also includes fixes for several bugs found in the original code:

### Critical Fixes
1. **Fixed typo** `needs_diplay_update` → `needs_display_update` (line 407 in original)
2. **Fixed missing parentheses** `epd.Clear` → `epd.Clear()` (initialization)
3. **Fixed comparison operator** `input_catchup==True` → `input_catchup = True`
4. **Added None check** for unmapped keyboard characters to prevent crashes
5. **Fixed word wrap edge case** when typing long words without spaces

### Improvements
6. **Added missing keyboard mappings**: `[` `]` `\` now work with Shift
7. **Improved scroll page counter** to prevent division by zero
8. **Added directory creation** for data folder if it doesn't exist
9. **Added CPU throttling** with `time.sleep(0.01)` to prevent 100% CPU usage
10. **Better error messages** in file loading

## Installation & Usage

### 1. Hardware Setup

Connect your 7.5" Waveshare V2 display to your Raspberry Pi using the same pins as the 4.2" version:

| Pin | BCM GPIO | Function |
|-----|----------|----------|
| RST | 17 | Reset |
| DC  | 25 | Data/Command |
| CS  | 8  | Chip Select |
| BUSY | 24 | Busy Signal |
| PWR | 18 | Power Control |

### 2. Software Setup

```bash
# Navigate to examples directory
cd e-Paper/RaspberryPi_JetsonNano/python/examples/

# Make sure the display driver is in place
# (epd7in5_V2_fast.py should already be copied to waveshare_epd/)

# Run the 7.5" version
python3 main_7in5.py
```

### 3. Optional: Set as Default

To make this the default startup application:

```bash
# Create a symlink or copy
cp main_7in5.py main.py

# Or edit your startup script to use main_7in5.py
```

## Usage Guide

The keyboard shortcuts are identical to the 4.2" version:

| Shortcut | Action |
|----------|--------|
| `Enter` | Save line and start new line (auto-saves to cache) |
| `Ctrl+S` | Manual save with timestamp |
| `Ctrl+N` | Create new document (saves current first) |
| `Ctrl+Esc` | Graceful shutdown |
| `↑` or `←` | Scroll up through previous text |
| `↓` or `→` | Scroll down through text |
| `Tab` | Insert two spaces |
| `Backspace` | Delete previous character |

## Display Performance

The 7.5" V2 Fast driver uses optimized LUT (Look-Up Table) values for faster partial refresh:

- **Full refresh**: ~2 seconds (clears ghosting)
- **Partial refresh**: ~0.5 seconds (active typing)
- **Refresh mode**: Automatically switches based on activity

### Refresh Behavior

1. **Startup**: Full refresh to clear screen
2. **Active typing**: Partial refresh of input line only (< 0.5s timeout)
3. **Scrolling**: Full screen update with previous text
4. **Saving**: Brief message displayed, then cleared

## File Storage

Files are stored in the same location as the 4.2" version:

- **Cache file**: `./data/cache.txt` (auto-saved on Enter)
- **Manual saves**: `./data/zw_YYYYMMDDHHMMSS.txt`
- **Access via network**: Set up Samba/SMB to access files remotely

## Performance Notes

### CPU Usage

The adapted version includes a `time.sleep(0.01)` in the main loop to prevent 100% CPU usage. This:
- Reduces power consumption
- Prevents thermal throttling on Pi Zero
- Has no noticeable impact on typing responsiveness

### Memory Usage

The larger display buffer requires more memory:
- **4.2" buffer**: 15,000 bytes
- **7.5" buffer**: 48,000 bytes

This is still well within the capabilities of even a Pi Zero.

## Customization

### Adjusting Font Size

To change the font size, edit `main_7in5.py`:

```python
font24 = ImageFont.truetype('Courier Prime.ttf', 24)  # Change 24 to desired size
```

If you change the font size, you'll also need to adjust:
- `linespacing` - Recommended: font_size + 4
- `chars_per_line` - Test to see what fits
- `lines_on_screen` - Calculate: (450 / linespacing)

### Example Configurations

**Smaller, more text (20pt)**:
```python
font24 = ImageFont.truetype('Courier Prime.ttf', 20)
linespacing = 24
chars_per_line = 76
lines_on_screen = 18
```

**Larger, easier reading (28pt)**:
```python
font24 = ImageFont.truetype('Courier Prime.ttf', 28)
linespacing = 32
chars_per_line = 54
lines_on_screen = 14
```

## Troubleshooting

### Display not working

1. **Check connections**: Verify all pins are properly connected
2. **Check display version**: This driver is for 7.5" **V2** only
   - For V1 displays, use `epd7in5.py` instead
3. **Check SPI**: Ensure SPI is enabled in `raspi-config`

```bash
sudo raspi-config
# Interface Options → SPI → Enable
```

### Display shows artifacts

Run a full clear cycle:

```python
# In Python shell
from waveshare_epd import epd7in5_V2_fast
epd = epd7in5_V2_fast.EPD()
epd.init()
epd.Clear()
epd.Clear()  # Run twice
```

### Text doesn't fit properly

Adjust the layout parameters as described in the Customization section above.

### Slow refresh rate

The 7.5" display is larger and will refresh slightly slower than the 4.2" version. This is normal. The fast LUT tables are already optimized for speed.

## Display Version Compatibility

### Identifying Your Display

Check the label on the back of your display:

- **7.5" V2**: Use `epd7in5_V2_fast.py` (this version)
- **7.5" HD**: Use `epd7in5_HD.py` (880×528 resolution)
- **7.5" V1**: Use `epd7in5.py`

### Switching Drivers

To use a different driver, edit `main_7in5.py`:

```python
# Current:
from waveshare_epd import epd7in5_V2_fast

# For HD version:
from waveshare_epd import epd7in5_HD
# Also update resolution to 880×528
```

## Known Limitations

1. **Display Size**: Larger display means:
   - Slower refresh times (~2× slower than 4.2")
   - Higher power consumption
   - Larger form factor

2. **Partial Refresh**: The fast LUT tables push the display outside recommended specs
   - Use at your own risk
   - May cause premature display aging
   - No warranty

3. **Ghosting**: After extended use without full refresh, you may see faint ghost images
   - Periodically trigger a full refresh with Ctrl+N
   - Or restart the application

## Credits

- **Original ZeroWriter**: See main project README
- **7.5" Adaptation**: Enhanced for larger display with bug fixes
- **Waveshare**: Display drivers and hardware
- **Ben Krasnow**: Fast LUT research for e-paper displays

## Support

For issues specific to the 7.5" version, please include:
- Display model number (check back label)
- Raspberry Pi model
- Full error messages
- Whether the original 4.2" code works

## License

Same as original ZeroWriter project - open source, free to modify and redistribute.
