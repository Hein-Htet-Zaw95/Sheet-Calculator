import streamlit as st
import math

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="面積計算機", 
    page_icon="📐", 
    layout="centered"
)

# ==============================================================================
# CONSTANTS & SPECIFICATIONS
# ==============================================================================

SHEET_SPECS = {
    'ceiling_thin': {
        'name': '養生シート 0.1mm × 1800mm × 50m',
        'width_mm': 1800,
        'length_m': 50,
        'thickness_mm': 0.1,
        'nominal_coverage': 90,
        'overlap_factor': 0.8,  # 20%重複
        'actual_coverage': 72,
        'description': '天井用 (1層)'
    },
    'ceiling_wide': {
        'name': '養生シート 0.1mm × 3600mm × 50m',
        'width_mm': 3600,
        'length_m': 50,
        'thickness_mm': 0.1,
        'nominal_coverage': 180,
        'overlap_factor': 0.8,  # 20%重複
        'actual_coverage': 144,
        'description': '天井用 (1層)'
    },
    'wall_thin': {
        'name': '養生シート 0.1mm × 1800mm × 50m',
        'width_mm': 1800,
        'length_m': 50,
        'thickness_mm': 0.1,
        'nominal_coverage': 90,
        'overlap_factor': 0.8,  # 20%重複
        'actual_coverage': 72,
        'description': '壁面用 (1層)'
    },
    'wall_wide': {
        'name': '養生シート 0.1mm × 3600mm × 50m',
        'width_mm': 3600,
        'length_m': 50,
        'thickness_mm': 0.1,
        'nominal_coverage': 180,
        'overlap_factor': 0.8,  # 20%重複
        'actual_coverage': 144,
        'description': '壁面用 (1層)'
    },
    'floor_thin': {
        'name': '養生シート 0.15mm × 1800mm × 50m',
        'width_mm': 1800,
        'length_m': 50,
        'thickness_mm': 0.15,
        'nominal_coverage': 90,
        'layers_required': 2,
        'actual_coverage': 36,  # 2層必要のため半分
        'description': '床面用 (2層必要)'
    },
    'floor_wide': {
        'name': '養生シート 0.15mm × 3600mm × 50m',
        'width_mm': 3600,
        'length_m': 50,
        'thickness_mm': 0.15,
        'nominal_coverage': 180,
        'layers_required': 2,
        'actual_coverage': 72,  # 2層必要のため半分
        'description': '床面用 (2層必要)'
    }
}

ROLL_WIDTH_1800 = 1800
ROLL_WIDTH_3600 = 3600
ROLL_LENGTH = 50

# ==============================================================================
# HELPER FUNCTIONS - ROLL CALCULATIONS
# ==============================================================================

def calculate_roll_combination_by_dimension(dimension_mm):
    """
    Calculate optimal roll combination based on a dimension (width for ceiling/floor).
    Returns the combination pattern, number of 1800mm rolls, and number of 3600mm rolls.
    
    Logic follows the specific pattern:
    - dimension ≤ 1200mm: use 1×1800mm
    - dimension ≤ 3000mm: use 1×3600mm
    - dimension 3000mm < 4500mm: use 1×3600mm + 1×1800mm
    - dimension 4500mm < 6300mm: use 2×3600mm
    - dimension 6300mm < 7800mm: use 2×3600mm + 1×1800mm
    - dimension 7800mm < 9600mm: use 3×3600mm
    - dimension 9600mm < 11100mm: use 3×3600mm + 1×1800mm
    - dimension 11100mm < 12900mm: use 4×3600mm
    - Continue pattern: alternate adding 3600mm then 1800mm until 100000mm
    """
    if dimension_mm <= 0:
        return [], 0, 0
    
    # Handle dimensions up to 100000mm with the specified pattern
    if dimension_mm <= 1200:
        rolls_1800, rolls_3600 = 1, 0
    elif dimension_mm <= 3000:
        rolls_1800, rolls_3600 = 0, 1
    elif dimension_mm <= 4500:
        rolls_1800, rolls_3600 = 1, 1
    elif dimension_mm <= 6300:
        rolls_1800, rolls_3600 = 0, 2
    elif dimension_mm <= 7800:
        rolls_1800, rolls_3600 = 1, 2
    elif dimension_mm <= 9600:
        rolls_1800, rolls_3600 = 0, 3
    elif dimension_mm <= 11100:
        rolls_1800, rolls_3600 = 1, 3
    elif dimension_mm <= 12900:
        rolls_1800, rolls_3600 = 0, 4
    elif dimension_mm <= 14400:
        rolls_1800, rolls_3600 = 1, 4
    elif dimension_mm <= 16200:
        rolls_1800, rolls_3600 = 0, 5
    elif dimension_mm <= 17700:
        rolls_1800, rolls_3600 = 1, 5
    elif dimension_mm <= 19500:
        rolls_1800, rolls_3600 = 0, 6
    elif dimension_mm <= 21000:
        rolls_1800, rolls_3600 = 1, 6
    elif dimension_mm <= 22800:
        rolls_1800, rolls_3600 = 0, 7
    elif dimension_mm <= 24300:
        rolls_1800, rolls_3600 = 1, 7
    elif dimension_mm <= 26100:
        rolls_1800, rolls_3600 = 0, 8
    elif dimension_mm <= 27600:
        rolls_1800, rolls_3600 = 1, 8
    elif dimension_mm <= 29400:
        rolls_1800, rolls_3600 = 0, 9
    elif dimension_mm <= 30900:
        rolls_1800, rolls_3600 = 1, 9
    elif dimension_mm <= 32700:
        rolls_1800, rolls_3600 = 0, 10
    elif dimension_mm <= 34200:
        rolls_1800, rolls_3600 = 1, 10
    elif dimension_mm <= 36000:
        rolls_1800, rolls_3600 = 0, 11
    elif dimension_mm <= 37500:
        rolls_1800, rolls_3600 = 1, 11
    elif dimension_mm <= 39300:
        rolls_1800, rolls_3600 = 0, 12
    elif dimension_mm <= 40800:
        rolls_1800, rolls_3600 = 1, 12
    elif dimension_mm <= 42600:
        rolls_1800, rolls_3600 = 0, 13
    elif dimension_mm <= 44100:
        rolls_1800, rolls_3600 = 1, 13
    elif dimension_mm <= 45900:
        rolls_1800, rolls_3600 = 0, 14
    elif dimension_mm <= 47400:
        rolls_1800, rolls_3600 = 1, 14
    elif dimension_mm <= 49200:
        rolls_1800, rolls_3600 = 0, 15
    elif dimension_mm <= 50700:
        rolls_1800, rolls_3600 = 1, 15
    elif dimension_mm <= 52500:
        rolls_1800, rolls_3600 = 0, 16
    elif dimension_mm <= 54000:
        rolls_1800, rolls_3600 = 1, 16
    elif dimension_mm <= 55800:
        rolls_1800, rolls_3600 = 0, 17
    elif dimension_mm <= 57300:
        rolls_1800, rolls_3600 = 1, 17
    elif dimension_mm <= 59100:
        rolls_1800, rolls_3600 = 0, 18
    elif dimension_mm <= 60600:
        rolls_1800, rolls_3600 = 1, 18
    elif dimension_mm <= 62400:
        rolls_1800, rolls_3600 = 0, 19
    elif dimension_mm <= 63900:
        rolls_1800, rolls_3600 = 1, 19
    elif dimension_mm <= 65700:
        rolls_1800, rolls_3600 = 0, 20
    elif dimension_mm <= 67200:
        rolls_1800, rolls_3600 = 1, 20
    elif dimension_mm <= 69000:
        rolls_1800, rolls_3600 = 0, 21
    elif dimension_mm <= 70500:
        rolls_1800, rolls_3600 = 1, 21
    elif dimension_mm <= 72300:
        rolls_1800, rolls_3600 = 0, 22
    elif dimension_mm <= 73800:
        rolls_1800, rolls_3600 = 1, 22
    elif dimension_mm <= 75600:
        rolls_1800, rolls_3600 = 0, 23
    elif dimension_mm <= 77100:
        rolls_1800, rolls_3600 = 1, 23
    elif dimension_mm <= 78900:
        rolls_1800, rolls_3600 = 0, 24
    elif dimension_mm <= 80400:
        rolls_1800, rolls_3600 = 1, 24
    elif dimension_mm <= 82200:
        rolls_1800, rolls_3600 = 0, 25
    elif dimension_mm <= 83700:
        rolls_1800, rolls_3600 = 1, 25
    elif dimension_mm <= 85500:
        rolls_1800, rolls_3600 = 0, 26
    elif dimension_mm <= 87000:
        rolls_1800, rolls_3600 = 1, 26
    elif dimension_mm <= 88800:
        rolls_1800, rolls_3600 = 0, 27
    elif dimension_mm <= 90300:
        rolls_1800, rolls_3600 = 1, 27
    elif dimension_mm <= 92100:
        rolls_1800, rolls_3600 = 0, 28
    elif dimension_mm <= 93600:
        rolls_1800, rolls_3600 = 1, 28
    elif dimension_mm <= 95400:
        rolls_1800, rolls_3600 = 0, 29
    elif dimension_mm <= 96900:
        rolls_1800, rolls_3600 = 1, 29
    elif dimension_mm <= 98700:
        rolls_1800, rolls_3600 = 0, 30
    elif dimension_mm <= 100000:
        rolls_1800, rolls_3600 = 1, 30
    else:
        # For dimensions > 100000mm, use algorithmic approach
        # Pattern: every 1800mm increment alternates between adding 3600mm and 1800mm
        base_3600_rolls = int(dimension_mm // 3600)
        remainder = dimension_mm % 3600
        
        if remainder <= 1200:
            rolls_1800 = 1 if remainder > 0 else 0
            rolls_3600 = base_3600_rolls
        else:
            # Need one more 3600mm roll for the remainder
            rolls_1800 = 0
            rolls_3600 = base_3600_rolls + 1
    
    # Build combination list for display
    combination = []
    for _ in range(rolls_3600):
        combination.append("3600mm")
    for _ in range(rolls_1800):
        combination.append("1800mm")
    
    return combination, rolls_1800, rolls_3600


def calculate_wall_roll_combination_by_dimension(dimension_mm, has_floor_covering=False):
    """
    Calculate optimal wall roll combination based on dimension and floor covering status.
    
    Args:
        dimension_mm: Wall dimension in millimeters
        has_floor_covering: Whether floor covering is being calculated
    
    Returns:
        tuple: (combination_list, rolls_1800, rolls_3600)
    
    Logic without floor covering:
    - dimension ≤ 1800mm: use 1×1800mm
    - dimension ≤ 3600mm: use 1×3600mm  
    - 3600mm < dimension ≤ 5400mm: use 1×3600mm + 1×1800mm
    - 5400mm < dimension ≤ 7200mm: use 2×3600mm
    - Continue pattern...
    
    Logic with floor covering:
    - dimension ≤ 2100mm: use 1×1800mm
    - dimension ≤ 3900mm: use 1×3600mm
    - 3900mm < dimension ≤ 5700mm: use 1×3600mm + 1×1800mm
    - 5700mm < dimension ≤ 7500mm: use 2×3600mm
    - Continue pattern...
    """
    if dimension_mm <= 0:
        return [], 0, 0
    
    rolls_1800 = 0
    rolls_3600 = 0
    remaining = dimension_mm
    
    # Set thresholds based on floor covering status
    if has_floor_covering:
        single_1800_threshold = 2100
        single_3600_threshold = 3900
        pattern_increment = 1800  # 2100 -> 3900 -> 5700 -> 7500...
    else:
        single_1800_threshold = 1800
        single_3600_threshold = 3600
        pattern_increment = 1800  # 1800 -> 3600 -> 5400 -> 7200...
    
    while remaining > 0:
        if remaining <= single_1800_threshold:
            rolls_1800 += 1
            remaining = 0
        elif remaining <= single_3600_threshold:
            rolls_3600 += 1
            remaining = 0
        elif remaining <= single_3600_threshold + pattern_increment:
            # Use 3600mm + 1800mm
            rolls_3600 += 1
            rolls_1800 += 1
            remaining = 0
        elif remaining <= single_3600_threshold + (2 * pattern_increment):
            # Use 2×3600mm
            rolls_3600 += 2
            remaining = 0
        else:
            # For larger dimensions, subtract one 3600mm and continue
            rolls_3600 += 1
            remaining -= 3600
            
            # If remainder is small enough for 1800mm, use it
            if remaining > 0 and remaining <= single_1800_threshold:
                rolls_1800 += 1
                remaining = 0
    
    # Build combination list for display
    combination = []
    for _ in range(rolls_3600):
        combination.append("3600mm")
    for _ in range(rolls_1800):
        combination.append("1800mm")
    
    return combination, rolls_1800, rolls_3600


def calculate_wall_rolls_by_height(height_mm, perimeter_m, has_floor_covering=False):
    """
    Calculate wall rolls based on height pattern and perimeter coverage.
    
    Args:
        height_mm: Wall height in millimeters
        perimeter_m: Room perimeter in meters
        has_floor_covering: Whether floor covering is being calculated
    
    Returns:
        tuple: (combination_list, rolls_1800_per_set, rolls_3600_per_set, num_sets)
    """
    if height_mm <= 0 or perimeter_m <= 0:
        return [], 0, 0, 0
    
    # Get the height-based roll pattern using wall-specific logic
    combination, rolls_1800_per_set, rolls_3600_per_set = calculate_wall_roll_combination_by_dimension(height_mm, has_floor_covering)
    
    # Calculate how many sets needed for perimeter coverage (50m per roll)
    num_sets = math.ceil(perimeter_m / ROLL_LENGTH)
    
    # Total rolls = pattern per set × number of sets
    total_rolls_1800 = rolls_1800_per_set * num_sets
    total_rolls_3600 = rolls_3600_per_set * num_sets
    
    return combination, total_rolls_1800, total_rolls_3600, num_sets


def calculate_floor_rolls_by_length(width_mm, length_m):
    """
    Calculate floor rolls based on width pattern and room length.
    Floor requires 2 layers, so length calculation is doubled.
    An additional 0.6m is added to the room length for safety margin/waste allowance.
    
    Args:
        width_mm: Room width in millimeters
        length_m: Room length in meters
    
    Returns:
        tuple: (combination_list, total_rolls_1800, total_rolls_3600)
    """
    if width_mm <= 0 or length_m <= 0:
        return [], 0, 0
    
    # Add 0.6m safety margin to room length
    adjusted_length_m = length_m + 0.6
    
    # Get the width-based roll pattern
    combination, rolls_1800_per_layer, rolls_3600_per_layer = calculate_roll_combination_by_dimension(width_mm)
    
    # Calculate total length needed (2 layers)
    total_rolls_1800 = 0
    total_rolls_3600 = 0
    
    if rolls_1800_per_layer > 0:
        length_needed_1800 = adjusted_length_m * 2 * rolls_1800_per_layer
        total_rolls_1800 = math.ceil(length_needed_1800 / ROLL_LENGTH)
    
    if rolls_3600_per_layer > 0:
        length_needed_3600 = adjusted_length_m * 2 * rolls_3600_per_layer
        total_rolls_3600 = math.ceil(length_needed_3600 / ROLL_LENGTH)
    
    return combination, total_rolls_1800, total_rolls_3600


def calculate_optimized_multi_room_floor(rooms_data):
    """
    Calculate optimized floor roll usage across ALL rooms.
    This function pools leftover material across rooms to minimize total rolls needed.
    
    Args:
        rooms_data: List of room dictionaries with floor_area, width_mm, length_m
    
    Returns:
        dict: Detailed breakdown including per-room usage and cross-room optimization
    """
    if not rooms_data:
        return {}, 0, 0
    
    # Track global leftover coverage that can be shared between rooms (in m²)
    global_leftover_1800_floor = 0
    global_leftover_3600_floor = 0
    
    # Track total rolls needed
    total_rolls_1800_floor = 0
    total_rolls_3600_floor = 0
    
    # Track detailed results per room
    floor_room_results = []
    
    # Floor coverage values (0.15mm thickness, 2 layers required)
    coverage_1800_floor = SHEET_SPECS['floor_thin']['actual_coverage']
    coverage_3600_floor = SHEET_SPECS['floor_wide']['actual_coverage']
    
    for room in rooms_data:
        room_name = room['name']
        floor_area = room.get('floor_area', 0)
        width_mm = room.get('width_mm', 0)
        length_m = room.get('length_m', 0)
        
        if floor_area <= 0 or width_mm <= 0 or length_m <= 0:
            continue
        
        # Get the width-based roll pattern
        combination, rolls_1800_per_layer, rolls_3600_per_layer = calculate_roll_combination_by_dimension(width_mm)
        
        # Calculate floor coverage needed (the actual_coverage already accounts for 2 layers)
        floor_1800_coverage_needed = 0
        floor_3600_coverage_needed = 0
        
        if floor_area > 0 and width_mm > 0:
            total_pattern_units = rolls_1800_per_layer + rolls_3600_per_layer
            if total_pattern_units > 0:
                # Do NOT double the area - actual_coverage already accounts for 2 layers
                floor_1800_coverage_needed = floor_area * (rolls_1800_per_layer / total_pattern_units)
                floor_3600_coverage_needed = floor_area * (rolls_3600_per_layer / total_pattern_units)
        
        # === TRY TO USE GLOBAL LEFTOVER FOR FLOOR FIRST ===
        floor_1800_from_leftover = 0
        floor_3600_from_leftover = 0
        
        if floor_1800_coverage_needed > 0 and global_leftover_1800_floor > 0:
            floor_1800_from_leftover = min(global_leftover_1800_floor, floor_1800_coverage_needed)
            global_leftover_1800_floor -= floor_1800_from_leftover
            floor_1800_coverage_needed -= floor_1800_from_leftover
        
        if floor_3600_coverage_needed > 0 and global_leftover_3600_floor > 0:
            floor_3600_from_leftover = min(global_leftover_3600_floor, floor_3600_coverage_needed)
            global_leftover_3600_floor -= floor_3600_from_leftover
            floor_3600_coverage_needed -= floor_3600_from_leftover
        
        # Calculate NEW rolls needed for remaining floor coverage
        new_floor_1800_rolls = 0
        new_floor_3600_rolls = 0
        new_leftover_1800_floor = 0
        new_leftover_3600_floor = 0
        
        # Use same approach as ceiling/wall: work entirely in coverage area (m²)
        if floor_1800_coverage_needed > 0:
            rolls_exact = floor_1800_coverage_needed / coverage_1800_floor
            new_floor_1800_rolls = math.ceil(rolls_exact)
            new_leftover_1800_floor = (new_floor_1800_rolls - rolls_exact) * coverage_1800_floor
        
        if floor_3600_coverage_needed > 0:
            rolls_exact = floor_3600_coverage_needed / coverage_3600_floor
            new_floor_3600_rolls = math.ceil(rolls_exact)
            new_leftover_3600_floor = (new_floor_3600_rolls - rolls_exact) * coverage_3600_floor
        
        # Add new leftovers to global pool
        global_leftover_1800_floor += new_leftover_1800_floor
        global_leftover_3600_floor += new_leftover_3600_floor
        
        # Update totals
        total_rolls_1800_floor += new_floor_1800_rolls
        total_rolls_3600_floor += new_floor_3600_rolls
        
        # Store results
        floor_room_results.append({
            'name': room_name,
            'floor_1800_from_leftover': floor_1800_from_leftover,
            'floor_3600_from_leftover': floor_3600_from_leftover,
            'new_floor_1800_rolls': new_floor_1800_rolls,
            'new_floor_3600_rolls': new_floor_3600_rolls,
            'room_total_1800': new_floor_1800_rolls,
            'room_total_3600': new_floor_3600_rolls,
            'floor_combination': combination
        })
    
    return {
        'floor_room_results': floor_room_results,
        'total_rolls_1800_floor': total_rolls_1800_floor,
        'total_rolls_3600_floor': total_rolls_3600_floor,
        'final_leftover_1800_floor': global_leftover_1800_floor,
        'final_leftover_3600_floor': global_leftover_3600_floor
    }, total_rolls_1800_floor, total_rolls_3600_floor


def calculate_optimized_multi_room_ceiling_wall(rooms_data, has_floor_covering=False):
    """
    Calculate optimized roll usage across ALL rooms for ceiling and walls.
    This function pools leftover material across rooms to minimize total rolls needed.
    
    Args:
        rooms_data: List of room dictionaries with ceiling_area, wall_area, width_mm, height_mm, perimeter
        has_floor_covering: Whether floor covering is being calculated (affects wall dimension logic)
    
    Returns:
        dict: Detailed breakdown including per-room usage and cross-room optimization
    """
    if not rooms_data:
        return {}, 0, 0
    
    # Track global leftover coverage that can be shared between rooms
    global_leftover_1800 = 0
    global_leftover_3600 = 0
    
    # Track total rolls needed
    total_rolls_1800 = 0
    total_rolls_3600 = 0
    
    # Track detailed results per room
    room_results = []
    
    # Coverage values
    coverage_1800 = SHEET_SPECS['ceiling_thin']['actual_coverage']
    coverage_3600 = SHEET_SPECS['ceiling_wide']['actual_coverage']
    
    for room in rooms_data:
        room_name = room['name']
        ceiling_area = room.get('ceiling_area', 0)
        wall_area = room.get('wall_area', 0)
        width_mm = room.get('width_mm', 0)
        height_mm = room.get('height_mm', 0)
        perimeter = room.get('perimeter', 0)
        
        if ceiling_area <= 0 and wall_area <= 0:
            continue
        
        # Get patterns
        ceiling_combination, ceiling_1800_pattern, ceiling_3600_pattern = \
            calculate_roll_combination_by_dimension(width_mm) if width_mm > 0 else ([], 0, 0)
        
        wall_combination, wall_1800_per_set, wall_3600_per_set, wall_perimeter_sets = \
            calculate_wall_rolls_by_height(height_mm, perimeter, has_floor_covering) if height_mm > 0 and perimeter > 0 else ([], 0, 0, 0)
        
        # Calculate ceiling coverage needed
        ceiling_1800_coverage_needed = 0
        ceiling_3600_coverage_needed = 0
        
        if ceiling_area > 0 and width_mm > 0:
            total_pattern_units = ceiling_1800_pattern + ceiling_3600_pattern
            if total_pattern_units > 0:
                ceiling_1800_coverage_needed = ceiling_area * (ceiling_1800_pattern / total_pattern_units)
                ceiling_3600_coverage_needed = ceiling_area * (ceiling_3600_pattern / total_pattern_units)
        
        # === TRY TO USE GLOBAL LEFTOVER FOR CEILING FIRST ===
        ceiling_1800_from_leftover = 0
        ceiling_3600_from_leftover = 0
        
        if ceiling_1800_coverage_needed > 0 and global_leftover_1800 > 0:
            ceiling_1800_from_leftover = min(global_leftover_1800, ceiling_1800_coverage_needed)
            global_leftover_1800 -= ceiling_1800_from_leftover
            ceiling_1800_coverage_needed -= ceiling_1800_from_leftover
        
        if ceiling_3600_coverage_needed > 0 and global_leftover_3600 > 0:
            ceiling_3600_from_leftover = min(global_leftover_3600, ceiling_3600_coverage_needed)
            global_leftover_3600 -= ceiling_3600_from_leftover
            ceiling_3600_coverage_needed -= ceiling_3600_from_leftover
        
        # Calculate NEW rolls needed for remaining ceiling coverage
        new_ceiling_1800_rolls = 0
        new_ceiling_3600_rolls = 0
        new_leftover_1800 = 0
        new_leftover_3600 = 0
        
        if ceiling_1800_coverage_needed > 0:
            rolls_exact = ceiling_1800_coverage_needed / coverage_1800
            new_ceiling_1800_rolls = math.ceil(rolls_exact)
            new_leftover_1800 = (new_ceiling_1800_rolls - rolls_exact) * coverage_1800
        
        if ceiling_3600_coverage_needed > 0:
            rolls_exact = ceiling_3600_coverage_needed / coverage_3600
            new_ceiling_3600_rolls = math.ceil(rolls_exact)
            new_leftover_3600 = (new_ceiling_3600_rolls - rolls_exact) * coverage_3600
        
        # Add new leftovers to global pool
        global_leftover_1800 += new_leftover_1800
        global_leftover_3600 += new_leftover_3600
        
        # === CALCULATE WALL NEEDS ===
        remaining_wall_area = wall_area
        
        # Try to use global leftover for walls
        wall_1800_from_leftover = 0
        wall_3600_from_leftover = 0
        
        if remaining_wall_area > 0 and global_leftover_1800 > 0:
            wall_1800_from_leftover = min(global_leftover_1800, remaining_wall_area)
            global_leftover_1800 -= wall_1800_from_leftover
            remaining_wall_area -= wall_1800_from_leftover
        
        if remaining_wall_area > 0 and global_leftover_3600 > 0:
            wall_3600_from_leftover = min(global_leftover_3600, remaining_wall_area)
            global_leftover_3600 -= wall_3600_from_leftover
            remaining_wall_area -= wall_3600_from_leftover
        
        # Calculate additional rolls for remaining wall area
        additional_wall_1800_rolls = 0
        additional_wall_3600_rolls = 0
        
        if remaining_wall_area > 0:
            if wall_1800_per_set > 0 or wall_3600_per_set > 0:
                pattern_coverage_per_set = (wall_3600_per_set * coverage_3600) + (wall_1800_per_set * coverage_1800)
                if pattern_coverage_per_set > 0:
                    sets_needed = math.ceil(remaining_wall_area / pattern_coverage_per_set)
                    additional_wall_3600_rolls = wall_3600_per_set * sets_needed
                    additional_wall_1800_rolls = wall_1800_per_set * sets_needed
                    
                    # Calculate leftover from these additional wall rolls
                    wall_coverage_provided = sets_needed * pattern_coverage_per_set
                    wall_leftover = wall_coverage_provided - remaining_wall_area
                    
                    # Distribute leftover proportionally
                    if wall_leftover > 0 and (wall_1800_per_set + wall_3600_per_set) > 0:
                        leftover_1800_portion = wall_leftover * (wall_1800_per_set / (wall_1800_per_set + wall_3600_per_set))
                        leftover_3600_portion = wall_leftover * (wall_3600_per_set / (wall_1800_per_set + wall_3600_per_set))
                        global_leftover_1800 += leftover_1800_portion
                        global_leftover_3600 += leftover_3600_portion
            else:
                # Fallback
                if remaining_wall_area >= coverage_3600:
                    additional_wall_3600_rolls = int(remaining_wall_area // coverage_3600)
                    remaining_after_3600 = remaining_wall_area % coverage_3600
                    if remaining_after_3600 > 0:
                        additional_wall_1800_rolls = 1
                        global_leftover_1800 += (coverage_1800 - remaining_after_3600)
                else:
                    additional_wall_1800_rolls = 1
                    global_leftover_1800 += (coverage_1800 - remaining_wall_area)
        
        # Update totals
        room_total_1800 = new_ceiling_1800_rolls + additional_wall_1800_rolls
        room_total_3600 = new_ceiling_3600_rolls + additional_wall_3600_rolls
        
        total_rolls_1800 += room_total_1800
        total_rolls_3600 += room_total_3600
        
        # Store results
        room_results.append({
            'name': room_name,
            'ceiling_1800_from_leftover': ceiling_1800_from_leftover,
            'ceiling_3600_from_leftover': ceiling_3600_from_leftover,
            'new_ceiling_1800_rolls': new_ceiling_1800_rolls,
            'new_ceiling_3600_rolls': new_ceiling_3600_rolls,
            'wall_1800_from_leftover': wall_1800_from_leftover,
            'wall_3600_from_leftover': wall_3600_from_leftover,
            'additional_wall_1800_rolls': additional_wall_1800_rolls,
            'additional_wall_3600_rolls': additional_wall_3600_rolls,
            'room_total_1800': room_total_1800,
            'room_total_3600': room_total_3600,
            'ceiling_combination': ceiling_combination,
            'wall_combination': wall_combination,
            'wall_perimeter_sets': wall_perimeter_sets
        })
    
    return {
        'room_results': room_results,
        'total_rolls_1800': total_rolls_1800,
        'total_rolls_3600': total_rolls_3600,
        'final_leftover_1800': global_leftover_1800,
        'final_leftover_3600': global_leftover_3600
    }, total_rolls_1800, total_rolls_3600


def calculate_optimized_multi_room_ceiling_wall_1800_only(rooms_data, has_floor_covering=False):
    """
    Calculate optimized roll usage across ALL rooms for ceiling and walls.
    ONLY uses 1800mm rolls (no 3600mm rolls).
    This function pools leftover material across rooms to minimize total rolls needed.
    
    Args:
        rooms_data: List of room dictionaries with ceiling_area, wall_area, width_mm, height_mm, perimeter
        has_floor_covering: Whether floor covering is being calculated
    
    Returns:
        dict: Detailed breakdown including per-room usage and cross-room optimization
    """
    if not rooms_data:
        return {}, 0, 0
    
    # Track global leftover coverage that can be shared between rooms
    global_leftover_1800 = 0
    
    # Track total rolls needed (only 1800mm)
    total_rolls_1800 = 0
    
    # Track detailed results per room
    room_results = []
    
    # Coverage values (only 1800mm)
    coverage_1800 = SHEET_SPECS['ceiling_thin']['actual_coverage']  # 72 m²
    
    for room in rooms_data:
        room_name = room['name']
        ceiling_area = room.get('ceiling_area', 0)
        wall_area = room.get('wall_area', 0)
        
        if ceiling_area <= 0 and wall_area <= 0:
            continue
        
        total_area_needed = ceiling_area + wall_area
        
        # === TRY TO USE GLOBAL LEFTOVER FIRST ===
        area_from_leftover = 0
        
        if total_area_needed > 0 and global_leftover_1800 > 0:
            area_from_leftover = min(global_leftover_1800, total_area_needed)
            global_leftover_1800 -= area_from_leftover
            total_area_needed -= area_from_leftover
        
        # Calculate NEW rolls needed for remaining area
        new_rolls_1800 = 0
        new_leftover_1800 = 0
        
        if total_area_needed > 0:
            rolls_exact = total_area_needed / coverage_1800
            new_rolls_1800 = math.ceil(rolls_exact)
            new_leftover_1800 = (new_rolls_1800 - rolls_exact) * coverage_1800
        
        # Add new leftovers to global pool
        global_leftover_1800 += new_leftover_1800
        
        # Update totals
        total_rolls_1800 += new_rolls_1800
        
        # Store results
        room_results.append({
            'name': room_name,
            'area_from_leftover': area_from_leftover,
            'new_rolls_1800': new_rolls_1800,
            'room_total_1800': new_rolls_1800,
            'room_total_3600': 0,  # No 3600mm rolls used
            'ceiling_combination': ["1800mm"] if ceiling_area > 0 else [],
            'wall_combination': ["1800mm"] if wall_area > 0 else []
        })
    
    return {
        'room_results': room_results,
        'total_rolls_1800': total_rolls_1800,
        'total_rolls_3600': 0,  # No 3600mm rolls
        'final_leftover_1800': global_leftover_1800,
        'final_leftover_3600': 0  # No 3600mm rolls
    }, total_rolls_1800, 0


def calculate_optimized_multi_room_floor_1800_only(rooms_data):
    """
    Calculate optimized floor roll usage across ALL rooms.
    ONLY uses 1800mm rolls (no 3600mm rolls).
    This function pools leftover material across rooms to minimize total rolls needed.
    
    Args:
        rooms_data: List of room dictionaries with floor_area, width_mm, length_m
    
    Returns:
        dict: Detailed breakdown including per-room usage and cross-room optimization
    """
    if not rooms_data:
        return {}, 0, 0
    
    # Track global leftover coverage that can be shared between rooms (in m²)
    global_leftover_1800_floor = 0
    
    # Track total rolls needed (only 1800mm)
    total_rolls_1800_floor = 0
    
    # Track detailed results per room
    floor_room_results = []
    
    # Floor coverage values (0.15mm thickness, 2 layers required) - only 1800mm
    coverage_1800_floor = SHEET_SPECS['floor_thin']['actual_coverage']  # 36 m²
    
    for room in rooms_data:
        room_name = room['name']
        floor_area = room.get('floor_area', 0)
        
        if floor_area <= 0:
            continue
        
        floor_coverage_needed = floor_area
        
        # === TRY TO USE GLOBAL LEFTOVER FOR FLOOR FIRST ===
        floor_from_leftover = 0
        
        if floor_coverage_needed > 0 and global_leftover_1800_floor > 0:
            floor_from_leftover = min(global_leftover_1800_floor, floor_coverage_needed)
            global_leftover_1800_floor -= floor_from_leftover
            floor_coverage_needed -= floor_from_leftover
        
        # Calculate NEW rolls needed for remaining floor coverage
        new_floor_1800_rolls = 0
        new_leftover_1800_floor = 0
        
        if floor_coverage_needed > 0:
            rolls_exact = floor_coverage_needed / coverage_1800_floor
            new_floor_1800_rolls = math.ceil(rolls_exact)
            new_leftover_1800_floor = (new_floor_1800_rolls - rolls_exact) * coverage_1800_floor
        
        # Add new leftovers to global pool
        global_leftover_1800_floor += new_leftover_1800_floor
        
        # Update totals
        total_rolls_1800_floor += new_floor_1800_rolls
        
        # Store results
        floor_room_results.append({
            'name': room_name,
            'floor_1800_from_leftover': floor_from_leftover,
            'floor_3600_from_leftover': 0,  # No 3600mm rolls
            'new_floor_1800_rolls': new_floor_1800_rolls,
            'new_floor_3600_rolls': 0,  # No 3600mm rolls
            'room_total_1800': new_floor_1800_rolls,
            'room_total_3600': 0,  # No 3600mm rolls
            'floor_combination': ["1800mm"] if floor_area > 0 else []
        })
    
    return {
        'floor_room_results': floor_room_results,
        'total_rolls_1800_floor': total_rolls_1800_floor,
        'total_rolls_3600_floor': 0,  # No 3600mm rolls
        'final_leftover_1800_floor': global_leftover_1800_floor,
        'final_leftover_3600_floor': 0  # No 3600mm rolls
    }, total_rolls_1800_floor, 0


# ==============================================================================
# HELPER FUNCTIONS - ROOM CALCULATIONS
# ==============================================================================

def calculate_room_metrics(length, width, height):
    """Calculate all metrics for a single room."""
    if length <= 0 or width <= 0 or height <= 0:
        return None
    
    floor_area = length * width
    ceiling_area = floor_area
    perimeter = 2 * (length + width)
    wall_area = perimeter * height
    
    return {
        'floor_area': floor_area,
        'ceiling_area': ceiling_area,
        'perimeter': perimeter,
        'wall_area': wall_area
    }

# ==============================================================================
# MAIN APP
# ==============================================================================

st.title("📐 面積計算機")

tab_room, tab_building, tab_sheets = st.tabs([
    "🏠 多室計算", 
    "🏗️ 外壁足場養生", 
    "🛡️ スマート養生シート"
])

# ==============================================================================
# TAB 1: MULTIPLE ROOMS
# ==============================================================================

with tab_room:
    st.header("🏠 多室計算機")
    
    # Initialize session state for rooms
    if 'rooms' not in st.session_state:
        st.session_state.rooms = [
            {'name': '部屋 1', 'length': 0.0, 'width': 0.0, 'height': 0.0}
        ]
    
    st.markdown("部屋を追加して設定してください:")
    
    # 部屋追加・削除ボタン
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("➕ 部屋を追加"):
            room_num = len(st.session_state.rooms) + 1
            st.session_state.rooms.append({
                'name': f'部屋 {room_num}',
                'length': 0.0,
                'width': 0.0,
                'height': 0.0
            })
            st.rerun()
    
    with col_btn2:
        if st.button("➖ 最後の部屋を削除") and len(st.session_state.rooms) > 1:
            st.session_state.rooms.pop()
            st.rerun()
    
    # Display rooms configuration
    rooms_data = []
    total_floor_area = 0
    total_ceiling_area = 0
    total_wall_area = 0
    
    for i, room in enumerate(st.session_state.rooms):
        st.markdown(f"### {room['name']}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            room['name'] = st.text_input(
                "部屋名", 
                value=room['name'], 
                key=f"name_{i}"
            )
        with col2:
            room['length'] = st.number_input(
                "長さ (m)", 
                min_value=0.0, 
                value=room['length'], 
                step=0.01, 
                format="%.4f",
                key=f"length_{i}"
            )
        with col3:
            room['width'] = st.number_input(
                "幅 (m)", 
                min_value=0.0, 
                value=room['width'], 
                step=0.01,
                format="%.4f",
                key=f"width_{i}"
            )
        with col4:
            room['height'] = st.number_input(
                "高さ (m)", 
                min_value=0.0, 
                value=room['height'], 
                step=0.01,
                format="%.4f",
                key=f"height_{i}"
            )
        
        # Calculate room metrics
        metrics = calculate_room_metrics(room['length'], room['width'], room['height'])
        
        if metrics:
            # Add to totals (always include all surfaces in Multi-Room tab)
            total_floor_area += metrics['floor_area']
            total_ceiling_area += metrics['ceiling_area']
            total_wall_area += metrics['wall_area']
            
            # Store room data (always include all areas)
            rooms_data.append({
                'name': room['name'],
                'floor_area': metrics['floor_area'],
                'ceiling_area': metrics['ceiling_area'],
                'wall_area': metrics['wall_area'],
                'perimeter': metrics['perimeter']
            })
            
            # Display individual room results (always show all)
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("床面積", f"{metrics['floor_area']:.2f} m²")
            with col_b:
                st.metric("天井面積", f"{metrics['ceiling_area']:.2f} m²")
            with col_c:
                st.metric("壁面積", f"{metrics['wall_area']:.2f} m²")
        
        st.markdown("---")
    
    # Display summary
    if rooms_data:
        st.subheader("📊 概要 - 全室")
        
        # Always show all surface totals in Multi-Room tab
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        with col_sum1:
            st.metric("**合計床面積**", f"{total_floor_area:.2f} m²")
        with col_sum2:
            st.metric("**合計天井面積**", f"{total_ceiling_area:.2f} m²")
        with col_sum3:
            st.metric("**合計壁面積**", f"{total_wall_area:.2f} m²")
        
        # Detailed breakdown table
        st.subheader("📋 部屋別内訳")
        
        # Always show all headers in Multi-Room tab
        col_headers = st.columns(5)
        headers = ["部屋名", "床面積 (m²)", "天井面積 (m²)", 
                   "壁面積 (m²)", "周囲長 (m)"]
        for col, header in zip(col_headers, headers):
            with col:
                st.write(f"**{header}**")
        
        for room_data in rooms_data:
            col_data = st.columns(5)
            with col_data[0]:
                st.write(room_data['name'])
            with col_data[1]:
                st.write(f"{room_data['floor_area']:.2f}")
            with col_data[2]:
                st.write(f"{room_data['ceiling_area']:.2f}")
            with col_data[3]:
                st.write(f"{room_data['wall_area']:.2f}")
            with col_data[4]:
                st.write(f"{room_data['perimeter']:.2f}")
    else:
        st.info("👆 少なくとも1つの部屋について、**長さ、幅、高さに正の値**を入力してください。")

# ==============================================================================
# TAB 2: 外壁足場養生 (EXTERIOR WALL PROTECTION)
# ==============================================================================

with tab_building:
    st.header("🏗️ 外壁足場養生計算機")
    
    # Initialize session state for building and scaffolding
    if 'building_config' not in st.session_state:
        st.session_state.building_config = {
            'building_length_m': 0.0,   # Default empty
            'building_height_m': 0.0,   # Default empty
            'scaffolding_length_m': 1.829, # Standard scaffolding length in meters
            'scaffolding_width_m': 0.9,    # Standard scaffolding width in meters
            'scaffolding_height_m': 1.725  # Standard scaffolding height in meters
        }
    
    st.markdown("**🏢 建物外壁寸法 (m):**")
    
    col_building1, col_building2 = st.columns(2)
    with col_building1:
        st.session_state.building_config['building_length_m'] = st.number_input(
            "建物長さ (m)", 
            min_value=0.0, 
            value=st.session_state.building_config['building_length_m'], 
            step=0.1,
            format="%.3f",
            key="building_length"
        )
    with col_building2:
        st.session_state.building_config['building_height_m'] = st.number_input(
            "建物高さ (m)", 
            min_value=0.0, 
            value=st.session_state.building_config['building_height_m'], 
            step=0.1,
            format="%.3f",
            key="building_height"
        )
    
    st.markdown("**🏗️ 足場寸法 (m):**")
    
    col_scaff1, col_scaff2, col_scaff3 = st.columns(3)
    with col_scaff1:
        st.session_state.building_config['scaffolding_length_m'] = st.number_input(
            "足場長さ (m)", 
            min_value=0.001, 
            value=st.session_state.building_config['scaffolding_length_m'], 
            step=0.001,
            format="%.3f",
            key="scaff_length"
        )
    with col_scaff2:
        st.session_state.building_config['scaffolding_width_m'] = st.number_input(
            "足場幅 (m)", 
            min_value=0.001, 
            value=st.session_state.building_config['scaffolding_width_m'], 
            step=0.001,
            format="%.3f",
            key="scaff_width"
        )
    with col_scaff3:
        st.session_state.building_config['scaffolding_height_m'] = st.number_input(
            "足場高さ (m)", 
            min_value=0.001, 
            value=st.session_state.building_config['scaffolding_height_m'], 
            step=0.001,
            format="%.3f",
            key="scaff_height"
        )
    
    # Calculate scaffolding requirements
    config = st.session_state.building_config
    
    if (config['building_length_m'] > 0 and config['building_height_m'] > 0 and 
        config['scaffolding_length_m'] > 0 and config['scaffolding_width_m'] > 0 and
        config['scaffolding_height_m'] > 0):
        
        # Calculate number of scaffolding units needed for ONE SIDE (always round UP)
        units_along_length = math.ceil(config['building_length_m'] / config['scaffolding_length_m'])
        units_along_height = math.ceil(config['building_height_m'] / config['scaffolding_height_m'])
        
        # Calculate scaffolding units for one side only
        total_side_units = units_along_length * units_along_height
        
        # Calculate coverage areas per scaffolding unit
        # Each unit covers: scaffolding_length × scaffolding_width (already in m²)
        unit_coverage_area = config['scaffolding_length_m'] * config['scaffolding_width_m']
        
        # Total coverage areas for one side
        total_top_area = total_side_units * unit_coverage_area      # Top (floor covering)
        total_bottom_area = total_side_units * unit_coverage_area   # Bottom (ceiling covering)
        
        # Calculate side wall coverage (足場側壁養生)
        # Total scaffolding length = units_along_length * scaffolding_length_m
        # Total scaffolding height = units_along_height * scaffolding_height_m
        total_scaffolding_length = units_along_length * config['scaffolding_length_m']
        total_scaffolding_height = units_along_height * config['scaffolding_height_m']
        side_wall_area = total_scaffolding_length * total_scaffolding_height
        
        # Calculate side wall horizontal covering details
        # Each 1800mm roll covers 1.8m width × 50m length horizontally
        roll_width_m = ROLL_WIDTH_1800 / 1000  # Convert 1800mm to 1.8m
        horizontal_strips_needed = math.ceil(total_scaffolding_height / roll_width_m)
        rolls_per_strip = math.ceil(total_scaffolding_length / ROLL_LENGTH)  # 50m per roll
        
        total_coverage_area = total_top_area + total_bottom_area + side_wall_area
        
        st.markdown("---")
        st.subheader("📊 足場ユニット計算")
        
        # Display calculation breakdown
        col_calc1, col_calc2, col_calc3 = st.columns(3)
        with col_calc1:
            st.markdown("**📐 必要ユニット数 (切り上げ):**")
            st.info(f"長さ: {config['building_length_m']:.3f}m ÷ {config['scaffolding_length_m']:.3f}m = **{units_along_length}** ユニット")
            st.info(f"高さ: {config['building_height_m']:.3f}m ÷ {config['scaffolding_height_m']:.3f}m = **{units_along_height}** ユニット")
        
        with col_calc2:
            st.markdown("**🏗️ 片面カバー範囲:**")
            st.write(f"長さユニット: {units_along_length}")
            st.write(f"高さユニット: {units_along_height}")
            st.metric("**片面ユニット**", f"{total_side_units}")
        
        with col_calc3:
            st.markdown("**📏 総カバー範囲:**")
            st.write(f"長さ × 高さ: {units_along_length} × {units_along_height}")
            st.metric("**総足場ユニット**", f"{total_side_units}")
            st.metric("**ユニット面積**", f"{unit_coverage_area:.3f} m²")
            st.caption("per ユニット")
            st.write(f"**側壁寸法:** {total_scaffolding_length:.3f}m × {total_scaffolding_height:.3f}m")
            st.write(f"**側壁ストリップ数:** {horizontal_strips_needed} 水平ストリップが必要")
            st.write(f"**ストリップ当たりロール数:** {rolls_per_strip} ロール (各50m長)")
        
        # Calculate roll requirements
        # Always use 1800mm rolls only for all surfaces in 外壁養生
        
        top_roll_coverage = SHEET_SPECS['floor_thin']['actual_coverage']      # 36 m² (2 layers, 0.15mm)
        bottom_roll_coverage = SHEET_SPECS['ceiling_thin']['actual_coverage']  # 72 m² (1 layer, 0.1mm)
        side_wall_roll_coverage = SHEET_SPECS['wall_thin']['actual_coverage']  # 72 m² (1 layer, 0.1mm)
        
        # Calculate rolls needed for each surface (all using 1800mm rolls)
        total_top_rolls = math.ceil(total_top_area / top_roll_coverage)
        total_bottom_rolls = math.ceil(total_bottom_area / bottom_roll_coverage)
        
        # Side wall calculation: Use pre-calculated horizontal covering values
        total_side_wall_rolls = horizontal_strips_needed * rolls_per_strip
        
        # Total rolls = sum of all surfaces (all 1800mm)
        total_all_rolls = total_top_rolls + total_bottom_rolls + total_side_wall_rolls
        
        st.subheader("📦 材料要件")
        
        col_mat1, col_mat2, col_mat3, col_mat4 = st.columns(4)
        with col_mat1:
            st.metric("**上部ロール (0.15mm)**", f"{total_top_rolls}")
            st.caption(f"{total_top_area:.1f} m² ÷ 36 = {total_top_rolls} × 1800mmロール")
        with col_mat2:
            st.metric("**下部ロール (0.1mm)**", f"{total_bottom_rolls}")  
            st.caption(f"{total_bottom_area:.1f} m² ÷ 72 = {total_bottom_rolls} × 1800mmロール")
        with col_mat3:
            st.metric("**側壁ロール (0.1mm)**", f"{total_side_wall_rolls}")
            st.caption(f"{horizontal_strips_needed} ストリップ × {rolls_per_strip} ロール/ストリップ = {total_side_wall_rolls} × 1800mmロール")
        with col_mat4:
            st.metric("**全ロール合計**", f"{total_all_rolls}")
            st.caption(f"全て1800mmロール: {total_all_rolls} 合計")
        
        # Display total coverage area separately with better formatting
        st.markdown("### 📏 **総カバー面積**")
        st.success(f"🎯 **{total_coverage_area:,.2f} m²** (上面: {total_top_area:.1f} + 下面: {total_bottom_area:.1f} + 側壁: {side_wall_area:.1f})")
        
        # Coverage options with safety margin
        st.subheader("🛡️ 材料概要")
        
        st.markdown("**📦 ロール必要数:**")
        st.success(f"🏢 **上面カバー（床）:** {total_top_rolls} ロール 0.15mm × 1800mm × 50m")
        st.success(f"🏠 **下面カバー（天井）:** {total_bottom_rolls} ロール 0.1mm × 1800mm × 50m")
        st.success(f"🧱 **側壁カバー:** {total_side_wall_rolls} ロール 0.1mm × 1800mm × 50m")
        
        st.info(f"**📊 総材料:** {total_all_rolls} ロール（すべて1800mm × 50m）")
        
        # Detailed breakdown table
        st.subheader("📋 計算詳細")
        
        # Create data for display
        calculation_data = {
            '建物長さ (m)': f"{config['building_length_m']:.3f}",
            '建物高さ (m)': f"{config['building_height_m']:.3f}",
            '足場長さ (m)': f"{config['scaffolding_length_m']:.3f}",
            '足場幅 (m)': f"{config['scaffolding_width_m']:.3f}",
            '足場高さ (m)': f"{config['scaffolding_height_m']:.3f}",
            '長さ方向ユニット数': units_along_length,
            '高さ方向ユニット数': units_along_height,
            '側面総ユニット数': total_side_units,
            '足場総長さ (m)': f"{total_scaffolding_length:.3f}",
            '足場総高さ (m)': f"{total_scaffolding_height:.3f}",
            '上面カバー面積 (m²)': f"{total_top_area:.2f}",
            '下面カバー面積 (m²)': f"{total_bottom_area:.2f}",
            '側壁面積 (m²)': f"{side_wall_area:.2f}",
            '総カバー面積 (m²)': f"{total_coverage_area:.2f}"
        }
        
        # Display as two-column layout
        col_table1, col_table2 = st.columns(2)
        
        with col_table1:
            st.markdown("**🏢 建物・足場寸法:**")
            for key, value in list(calculation_data.items())[:9]:
                st.write(f"• **{key}:** {value}")
        
        with col_table2:
            st.markdown("**📊 カバー面積計算:**")
            for key, value in list(calculation_data.items())[9:]:
                st.write(f"• **{key}:** {value}")
        
        # Store data for integration with 養生シート calculator  
        scaffolding_data = [{
            'name': '建物足場カバー',
            'length': config['scaffolding_length_m'],  # Already in meters
            'width': config['scaffolding_width_m'],
            'height': config['scaffolding_height_m'],
            'top_area': total_top_area,
            'bottom_area': total_bottom_area,
            'side_wall_area': side_wall_area,
            'total_scaffolding_length': total_scaffolding_length,
            'total_scaffolding_height': total_scaffolding_height,
            'total_coverage_area': total_coverage_area,
            'volume': total_side_units * unit_coverage_area * config['scaffolding_height_m'],
            'total_top_rolls': total_top_rolls,
            'total_bottom_rolls': total_bottom_rolls,
            'total_side_wall_rolls': total_side_wall_rolls,
            'horizontal_strips_needed': horizontal_strips_needed,
            'rolls_per_strip': rolls_per_strip,
            'roll_type': '1800mmのみ - 水平カバー'
        }]
        
        # Store in session state for 養生シート tab integration
        st.session_state['scaffolding_data'] = scaffolding_data
        
    else:
        st.info("👆 すべての建物および足場寸法に**正の値**を入力してください。")

# ==============================================================================
# TAB 3: SMART 養生シート CALCULATOR  
# ==============================================================================

with tab_sheets:
    st.header("🛡️ スマート養生シート計算機")
    
    # Import data from other tabs
    st.subheader("📥 部屋データの取り込み")
    
    if st.button("📂 多室データを取り込み", use_container_width=True):
        if 'rooms' in st.session_state and st.session_state.rooms:
            # Process room data for Smart calculator
            imported_rooms = []
            for room in st.session_state.rooms:
                metrics = calculate_room_metrics(room['length'], room['width'], room['height'])
                if metrics:
                    imported_rooms.append({
                        'name': room['name'],
                        'floor_area': metrics['floor_area'],
                        'ceiling_area': metrics['ceiling_area'],
                        'wall_area': metrics['wall_area'],
                        'perimeter': metrics['perimeter'],
                        'width_mm': room['width'] * 1000,  # Convert to mm
                        'height_mm': room['height'] * 1000,  # Convert to mm
                        'length_m': room['length']
                    })
            
            if imported_rooms:
                st.session_state['imported_rooms'] = imported_rooms
                st.success(f"✅ {len(imported_rooms)}室を正常に取り込みました！")
                st.rerun()
            else:
                st.error("❌ 有効な部屋データが見つかりませんでした。")
        else:
            st.error("❌ 利用可能な部屋データがありません。まず多室タブで部屋を設定してください。")
    
    # Display imported rooms
    if 'imported_rooms' in st.session_state and st.session_state.imported_rooms:
        st.subheader("📋 取り込み済み部屋/エリア")
        
        for i, room in enumerate(st.session_state.imported_rooms):
            col_room = st.columns([3, 1])
            with col_room[0]:
                st.write(f"**{room['name']}** - 床: {room['floor_area']:.2f}m², 天井: {room['ceiling_area']:.2f}m², 壁: {room['wall_area']:.2f}m²")
            with col_room[1]:
                if st.button("🗑️", key=f"remove_{i}", help="この部屋を削除"):
                    st.session_state.imported_rooms.pop(i)
                    st.rerun()
        
        st.markdown("---")
        
        # Multi-room optimization section
        st.subheader("🚀 AI搭載多室最適化")
        
        # Surface selection checkboxes
        st.markdown("**📊 計算する面を選択してください:**")
        col_surface1, col_surface2, col_surface3 = st.columns(3)
        
        with col_surface1:
            include_floor_calc = st.checkbox("🏠 床面積", value=True, key="calc_include_floor")
        with col_surface2:
            include_ceiling_calc = st.checkbox("🏠 天井面積", value=True, key="calc_include_ceiling")  
        with col_surface3:
            include_wall_calc = st.checkbox("🧱 壁面積", value=True, key="calc_include_wall")
        
        if st.button("🧮 最適化ロール要件を計算", use_container_width=True, type="primary"):
            # Filter imported rooms based on surface selection
            rooms_for_calc = []
            for room in st.session_state.imported_rooms:
                filtered_room = {
                    'name': room['name'],
                    'perimeter': room['perimeter'],
                    'width_mm': room['width_mm'],
                    'height_mm': room['height_mm'], 
                    'length_m': room['length_m']
                }
                
                # Apply surface selection filters
                if include_floor_calc:
                    filtered_room['floor_area'] = room.get('floor_area', 0)
                else:
                    filtered_room['floor_area'] = 0
                    
                if include_ceiling_calc:
                    filtered_room['ceiling_area'] = room.get('ceiling_area', 0)
                else:
                    filtered_room['ceiling_area'] = 0
                    
                if include_wall_calc:
                    filtered_room['wall_area'] = room.get('wall_area', 0)
                else:
                    filtered_room['wall_area'] = 0
                
                rooms_for_calc.append(filtered_room)
            
            # Always use Mixed Roll Sizes for multi-room optimization
            # Calculate ceiling + wall optimization (use floor checkbox for wall calculation logic)
            ceiling_wall_results, total_cw_1800, total_cw_3600 = calculate_optimized_multi_room_ceiling_wall(rooms_for_calc, include_floor_calc)
            
            # Calculate floor optimization if floor is enabled
            floor_results = {}
            total_floor_1800 = 0
            total_floor_3600 = 0
            
            if include_floor_calc:
                floor_results, total_floor_1800, total_floor_3600 = calculate_optimized_multi_room_floor(rooms_for_calc)
            
            # Combined totals
            grand_total_1800 = total_cw_1800 + total_floor_1800
            grand_total_3600 = total_cw_3600 + total_floor_3600
            
            # Display results summary with thickness breakdown
            st.subheader("📦 最適化ロール概要")
            
            # Calculate rolls by thickness
            ceiling_wall_1800_01mm = total_cw_1800  # Ceiling/wall uses 0.1mm
            ceiling_wall_3600_01mm = total_cw_3600  # Ceiling/wall uses 0.1mm
            floor_1800_015mm = total_floor_1800 if include_floor_calc else 0  # Floor uses 0.15mm
            floor_3600_015mm = total_floor_3600 if include_floor_calc else 0  # Floor uses 0.15mm
            
            col_summary = st.columns(5)
            with col_summary[0]:
                st.metric("**1800mm × 0.1mm**", f"{ceiling_wall_1800_01mm}")
                st.caption("天井・壁カバー")
            with col_summary[1]:
                st.metric("**1800mm × 0.15mm**", f"{floor_1800_015mm}")
                st.caption("床カバー (2層)")
            with col_summary[2]:
                st.metric("**3600mm × 0.1mm**", f"{ceiling_wall_3600_01mm}")
                st.caption("天井・壁カバー")
            with col_summary[3]:
                st.metric("**3600mm × 0.15mm**", f"{floor_3600_015mm}")
                st.caption("床カバー (2層)")
            with col_summary[4]:
                total_rolls = grand_total_1800 + grand_total_3600
                st.metric("**総ロール数**", f"{total_rolls}")
                st.caption("全厚さ・サイズ")
            
            # Additional summary breakdown
            st.markdown("### 📊 **用途別ロール概要**")
            col_app = st.columns(3)
            with col_app[0]:
                ceiling_wall_total = ceiling_wall_1800_01mm + ceiling_wall_3600_01mm
                st.info(f"🏠 **天井・壁:** {ceiling_wall_total} ロール (0.1mm)")
                if ceiling_wall_1800_01mm > 0:
                    st.write(f"• {ceiling_wall_1800_01mm} × 1800mm × 0.1mm")
                if ceiling_wall_3600_01mm > 0:
                    st.write(f"• {ceiling_wall_3600_01mm} × 3600mm × 0.1mm")
            
            with col_app[1]:
                if include_floor_calc:
                    floor_total = floor_1800_015mm + floor_3600_015mm
                    st.info(f"🏢 **床:** {floor_total} ロール (0.15mm)")
                    if floor_1800_015mm > 0:
                        st.write(f"• {floor_1800_015mm} × 1800mm × 0.15mm")
                    if floor_3600_015mm > 0:
                        st.write(f"• {floor_3600_015mm} × 3600mm × 0.15mm")
                else:
                    st.info("🏢 **床:** 含まれていません")
            
            with col_app[2]:
                st.success(f"📦 **総合計:** {total_rolls} ロール")
                st.write(f"• **1800mm:** {grand_total_1800} ロール")
                st.write(f"• **3600mm:** {grand_total_3600} ロール")
            
            # Detailed breakdown
            if ceiling_wall_results and 'room_results' in ceiling_wall_results:
                st.subheader("🏠 天井・壁内訳")
                
                for room_result in ceiling_wall_results['room_results']:
                    with st.expander(f"📋 {room_result['name']} 詳細"):
                        col_detail = st.columns(2)
                        with col_detail[0]:
                            st.write("**天井カバー:**")
                            if room_result.get('ceiling_1800_from_leftover', 0) > 0:
                                st.write(f"• 余りから: {room_result['ceiling_1800_from_leftover']:.1f} m² (1800mm)")
                            if room_result.get('ceiling_3600_from_leftover', 0) > 0:
                                st.write(f"• 余りから: {room_result['ceiling_3600_from_leftover']:.1f} m² (3600mm)")
                            if room_result.get('new_ceiling_1800_rolls', 0) > 0:
                                st.write(f"• 新規ロール: {room_result['new_ceiling_1800_rolls']} × 1800mm")
                            if room_result.get('new_ceiling_3600_rolls', 0) > 0:
                                st.write(f"• 新規ロール: {room_result['new_ceiling_3600_rolls']} × 3600mm")
                        
                        with col_detail[1]:
                            st.write("**壁カバー:**")
                            if room_result.get('wall_1800_from_leftover', 0) > 0:
                                st.write(f"• 余りから: {room_result['wall_1800_from_leftover']:.1f} m² (1800mm)")
                            if room_result.get('wall_3600_from_leftover', 0) > 0:
                                st.write(f"• 余りから: {room_result['wall_3600_from_leftover']:.1f} m² (3600mm)")
                            if room_result.get('additional_wall_1800_rolls', 0) > 0:
                                st.write(f"• 追加ロール: {room_result['additional_wall_1800_rolls']} × 1800mm")
                            if room_result.get('additional_wall_3600_rolls', 0) > 0:
                                st.write(f"• 追加ロール: {room_result['additional_wall_3600_rolls']} × 3600mm")
            
            if include_floor_calc and floor_results and 'floor_room_results' in floor_results:
                st.subheader("🏢 床カバー内訳")
                
                for room_result in floor_results['floor_room_results']:
                    with st.expander(f"📋 {room_result['name']} 床詳細"):
                        col_floor = st.columns(2)
                        with col_floor[0]:
                            st.write("**床カバー (2層):**")
                            if room_result.get('floor_1800_from_leftover', 0) > 0:
                                st.write(f"• 余りから: {room_result['floor_1800_from_leftover']:.1f} m² (1800mm)")
                            if room_result.get('floor_3600_from_leftover', 0) > 0:
                                st.write(f"• 余りから: {room_result['floor_3600_from_leftover']:.1f} m² (3600mm)")
                        
                        with col_floor[1]:
                            st.write("**必要新規ロール:**")
                            if room_result.get('new_floor_1800_rolls', 0) > 0:
                                st.write(f"• 新規ロール: {room_result['new_floor_1800_rolls']} × 1800mm")
                            if room_result.get('new_floor_3600_rolls', 0) > 0:
                                st.write(f"• 新規ロール: {room_result['new_floor_3600_rolls']} × 3600mm")
            
            # Leftover material summary
            st.subheader("♻️ 残余材料")
            
            col_leftover = st.columns(2)
            with col_leftover[0]:
                if ceiling_wall_results:
                    leftover_1800 = ceiling_wall_results.get('final_leftover_1800', 0)
                    leftover_3600 = ceiling_wall_results.get('final_leftover_3600', 0)
                    st.write(f"**天井・壁余り:**")
                    st.write(f"• 1800mmカバー: {leftover_1800:.1f} m²")
                    st.write(f"• 3600mmカバー: {leftover_3600:.1f} m²")
            
            with col_leftover[1]:
                if include_floor_calc and floor_results:
                    leftover_floor_1800 = floor_results.get('final_leftover_1800_floor', 0)
                    leftover_floor_3600 = floor_results.get('final_leftover_3600_floor', 0)
                    st.write(f"**床余り:**")
                    st.write(f"• 1800mmカバー: {leftover_floor_1800:.1f} m²")
                    st.write(f"• 3600mmカバー: {leftover_floor_3600:.1f} m²")
        
    else:
        st.info("📥 スマート最適化を開始するには、**多室または外壁足場養生タブから部屋データを取り込み**してください。")
        st.markdown("""
        **🚀 スマート機能:**
        - 🔄 室間材料最適化
        - 💰 廃棄物最小化アルゴリズム  
        - 🎯 インテリジェントロールサイズ選択
        - 📊 詳細カバレッジ内訳
        """)

# ==============================================================================
# FOOTER
# ==============================================================================

st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; font-size: 0.8em; margin-top: 2rem;">
    📐 面積計算機 | 🛡️ スマート養生シート最適化 | 🏗️ 外壁足場養生計画
    </div>
    """, 
    unsafe_allow_html=True
)
