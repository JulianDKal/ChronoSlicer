def rgb_to_hex(color_tuple):
    """Convert PyMuPDF RGB tuple (0-1 range) to hex color string"""
    if color_tuple is None:
        return None
    return '#{:02x}{:02x}{:02x}'.format(
        int(color_tuple[0] * 255),
        int(color_tuple[1] * 255),
        int(color_tuple[2] * 255)
    )