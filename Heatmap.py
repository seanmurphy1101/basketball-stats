import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc, Wedge
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
from PIL import Image
from shapely.geometry import Point, Polygon
import math


def findLine(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - (m * x1)
    return m, b

def checkPointInSector(radius, x, y, startAngle, endAngle):
    # Calculate polar coordinates
    polarradius = math.sqrt(x * x + y * y)
    if x == 0 and y >= 0:
        Angle = 90
    elif x == 0 and y < 0:
        Angle = 270
    else:
        Angle = math.degrees(math.atan(y / x))
    
    # Adjust angle depending on what quadrant the point is in
    if x <= 0:
        Angle = 180 + Angle
    elif x > 0 and y < 0:
        Angle = 360 + Angle
        
    # Check whether polarradius is less then radius of circle or not
    # and Angle is between startAngle and endAngle or not
    if (Angle >= startAngle and Angle <= endAngle
                        and polarradius < radius):
        return True
    else:
        return False

    
def calculateZones(df):
    zone_1_make = 0
    zone_1_miss = 0
    zone_2_make = 0
    zone_2_miss = 0
    zone_3_make = 0
    zone_3_miss = 0
    zone_4_make = 0
    zone_4_miss = 0
    zone_5_make = 0
    zone_5_miss = 0
    zone_6_make = 0
    zone_6_miss = 0
    zone_7_make = 0
    zone_7_miss = 0
    zone_8_make = 0
    zone_8_miss = 0
    zone_9_make = 0
    zone_9_miss = 0
    for index, row in df.iterrows():
        x_loc = -row.y
        y_loc = row.x
        miss = row.missed
        
        point = Point(x_loc, y_loc)
        x_hoop = 0
        y_hoop = 41.75
        dist = math.sqrt((x_loc - x_hoop)**2 + (y_loc - y_hoop)**2)
        point_rel_hoop = (x_loc, y_loc-y_hoop)

        zone_2_polygon = Polygon([(-19.75, 47), (-19.75, 41.75), (-6, 41.75), (-6, 47)])
        zone_4_polygon = Polygon([(19.75, 47), (19.75, 41.75), (6, 41.75), (6, 47)])
        zone_5_polygon1 = Polygon([(-25, 47), (-25, 41.75), (-19.75, 41.75), (-19.75, 47)])
        zone_5_polygon2 = Polygon([(-25, 41.75), (-25, 36.1), (-18.9246, 36.1), (-19.75, 41.75)])
        zone_6_polygon = Polygon([(-25, 36.1), (-25, 0), (-17.93, 0), (-8.2, 23.8), (-18.9246, 36.1)])
        zone_7_polygon = Polygon([(-8.2, 23.8), (-17.93, 0), (17.93, 0), (8.2, 23.8)])
        zone_8_polygon = Polygon([(25, 36.1), (25, 0), (17.93, 0), (8.2, 23.8), (18.9246, 36.1)])
        zone_9_polygon1 = Polygon([(25, 47), (25, 41.75), (19.75, 41.75), (19.75, 47)])
        zone_9_polygon2 = Polygon([(25, 41.75), (25, 36.1), (18.9246, 36.1), (19.75, 41.75)])

        if dist <= 8:
            if miss:
                zone_1_miss += 1
            else:
                zone_1_make += 1
        elif (dist > 8) and (point.within(zone_2_polygon) or checkPointInSector(19.75, point_rel_hoop[0], point_rel_hoop[1], 180, 226.27)):
            if miss:
                zone_2_miss += 1
            else:
                zone_2_make += 1
        elif (dist > 8) and (checkPointInSector(19.75, point_rel_hoop[0], point_rel_hoop[1], 226.27, 313.73)):
            if miss:
                zone_3_miss += 1
            else:
                zone_3_make += 1
        elif (dist > 8) and (point.within(zone_4_polygon) or checkPointInSector(19.75, point_rel_hoop[0], point_rel_hoop[1], 313.73, 360)):
            if miss:
                zone_4_miss += 1
            else:
                zone_4_make += 1
        elif point.within(zone_5_polygon1) or (dist > 19.75 and point.within(zone_5_polygon2)):
            if miss:
                zone_5_miss += 1
            else:
                zone_5_make += 1
        elif dist > 19.75 and point.within(zone_6_polygon):
            if miss:
                zone_6_miss += 1
            else:
                zone_6_make += 1
        elif dist > 19.75 and point.within(zone_7_polygon):
            if miss:
                zone_7_miss += 1
            else:
                zone_7_make += 1
        elif dist > 19.75 and point.within(zone_8_polygon):
            if miss:
                zone_8_miss += 1
            else:
                zone_8_make += 1
        elif point.within(zone_9_polygon1) or (dist > 19.75 and point.within(zone_9_polygon2)):
            if miss:
                zone_9_miss += 1
            else:
                zone_9_make += 1
                
    zone_1_shots = zone_1_make + zone_1_miss
    zone_2_shots = zone_2_make + zone_2_miss
    zone_3_shots = zone_3_make + zone_3_miss
    zone_4_shots = zone_4_make + zone_4_miss
    zone_5_shots = zone_5_make + zone_5_miss
    zone_6_shots = zone_6_make + zone_6_miss
    zone_7_shots = zone_7_make + zone_7_miss
    zone_8_shots = zone_8_make + zone_8_miss
    zone_9_shots = zone_9_make + zone_9_miss
    
    if (zone_1_shots) == 0:
        zone_1_percent = -1
        zone_1_text = None
    else:
        zone_1_percent = round((zone_1_make / (zone_1_shots)) * 100)
        zone_1_text = f'{zone_1_make} / {zone_1_make + zone_1_miss} \n \n {zone_1_percent}%'
        
    if (zone_2_shots) == 0:
        zone_2_percent = -1
        zone_2_text = None
    else:
        zone_2_percent = round((zone_2_make / (zone_2_shots)) * 100)
        zone_2_text = f'{zone_2_make} / {zone_2_make + zone_2_miss} \n \n {zone_2_percent}%'
        
    if (zone_3_shots) == 0:
        zone_3_percent = -1
        zone_3_text = None
    else:
        zone_3_percent = round((zone_3_make / (zone_3_shots)) * 100)
        zone_3_text = f'{zone_3_make} / {zone_3_make + zone_3_miss} \n \n {zone_3_percent}%'
        
    if (zone_4_shots) == 0:
        zone_4_percent = -1
        zone_4_text = None
    else:
        zone_4_percent = round((zone_4_make / (zone_4_shots)) * 100)
        zone_4_text = f'{zone_4_make} / {zone_4_make + zone_4_miss} \n \n {zone_4_percent}%'
        
    if (zone_5_shots) == 0:
        zone_5_percent = -1
        zone_5_text = None
    else:
        zone_5_percent = round((zone_5_make / (zone_5_shots)) * 100)
        zone_5_text = f'{zone_5_make} / {zone_5_make + zone_5_miss} \n \n {zone_5_percent}%'
        
    if (zone_6_shots) == 0:
        zone_6_percent = -1
        zone_6_text = None
    else:
        zone_6_percent = round((zone_6_make / (zone_6_shots)) * 100)
        zone_6_text = f'{zone_6_make} / {zone_6_make + zone_6_miss} \n \n {zone_6_percent}%'
        
    if (zone_7_shots) == 0:
        zone_7_percent = -1
        zone_7_text = None
    else:
        zone_7_percent = round((zone_7_make / (zone_7_shots)) * 100)
        zone_7_text = f'{zone_7_make} / {zone_7_make + zone_7_miss} \n \n {zone_7_percent}%'
        
    if (zone_8_shots) == 0:
        zone_8_percent = -1
        zone_8_text = None
    else:
        zone_8_percent = round((zone_8_make / (zone_8_shots)) * 100)
        zone_8_text = f'{zone_8_make} / {zone_8_make + zone_8_miss} \n \n {zone_8_percent}%'
        
    if (zone_9_shots) == 0:
        zone_9_percent = -1
        zone_9_text = None
    else:
        zone_9_percent = round((zone_9_make / (zone_9_shots)) * 100)
        zone_9_text = f'{zone_9_make} / {zone_9_make + zone_9_miss} \n \n {zone_9_percent}%'
        
    zone_percent_list = [zone_1_percent, zone_2_percent, zone_3_percent, zone_4_percent, zone_5_percent, zone_6_percent, zone_7_percent, zone_8_percent, zone_9_percent]
    zone_colors = []
    
    for i in range(len(zone_percent_list)):
        # restricted area
        if i == 0:
            if zone_percent_list[i] >= 60:
                zone_colors.append('red')
            elif zone_percent_list[i] >= 50:
                zone_colors.append('yellow')
            else:
                zone_colors.append('blue')
        # 2-point zones
        elif i < 4:
            if zone_percent_list[i] >= 50:
                zone_colors.append('red')
            elif zone_percent_list[i] >= 40:
                zone_colors.append('yellow')
            else:
                zone_colors.append('blue')
        # 3-point zones
        else:
            if zone_percent_list[i] >= 37.5:
                zone_colors.append('red')
            elif zone_percent_list[i] >= 30:
                zone_colors.append('yellow')
            else:
                zone_colors.append('blue')
            
                
    return zone_1_text, zone_2_text, zone_3_text, zone_4_text, zone_5_text, zone_6_text, zone_7_text, zone_8_text, zone_9_text, zone_colors

def draw_court_vertical_heatmap(df, name, file_path, color="black", lw=2, zorder=1):
    global fig, ax
    img = Image.open("basketball_court_background.jpg")
    img = img.rotate(90, expand=True)
    
    fig=plt.figure(figsize=(12.0,10.0))
    ax=fig.add_subplot(1,1,1)
    im = ax.imshow(img, extent=[-30,30,-5,50])
    ax = plt.gca()
        
    # Creates the out of bounds lines around the half court
    outer = Rectangle((-25,0), width=50, height=47, color=color,
                      zorder=zorder, fill=False, lw=lw)
    
    # Creates the center circles and center line
    center_circle = Circle((0, 0), radius=6, lw=lw, fill=False,
                           color=color, zorder=zorder)

    # Center line
    ax.plot([-25,25],[0,0], color=color, zorder=zorder, lw=lw)
    
    # The dash lines near the middle of the court (Idk what they are called)
    ax.plot([-25,-22],[19,19], color=color, zorder=zorder, lw=lw)
    ax.plot([22,25],[19,19], color=color, zorder=zorder, lw=lw)
    
    # Paint Area
    box = Rectangle((-6, 28), 12, 19, lw=lw, fill=False,
                            color=color, zorder=zorder)
    
    # Left and right free throw circles
    free_throw_fill = Arc((0,28), 12, 12, theta1=180, theta2=360, lw=lw, fill=False,
                          color=color, zorder=zorder)
    free_throw_dash = Arc((0,28), 12, 12, theta1=0, theta2=180, lw=lw, fill=False, color=color,
                            zorder=zorder, linestyle='dashed')
    
    # Backboard
    ax.plot([3,-3],[43,43], color=color, zorder=zorder, lw=1)
    
    # Hoop
    hoop = Circle((0,41.75), radius=0.75, lw=1, fill=False, 
                    color=color, zorder=zorder)
    
    # Straight part of corner 3pt lines
    ax.plot([-19.75,-19.75],[47,41.75], color=color, zorder=zorder, lw=lw)
    ax.plot([19.75,19.75],[47,41.75], color=color, zorder=zorder, lw=lw)
    
    # 3pt Arc
    arc = Arc((0,41.75), 39.5, 39.5, theta1=180, theta2=360, lw=lw,
                color=color, zorder=zorder)
    
    # Extra Lines
    top_rect = Rectangle((6,40), 0.7, 1, lw=lw, fill=True, color=color, zorder=zorder)
    bottom_rect = Rectangle((-6.7,40), 0.7, 1, lw=lw, fill=True, color=color, zorder=zorder)
    ax.plot([6,6.7],[36,36], color=color, zorder=zorder, lw=lw)
    ax.plot([-6,-6.7],[36,36], color=color, zorder=zorder, lw=lw)
    ax.plot([6,6.7],[33,33], color=color, zorder=zorder, lw=lw)
    ax.plot([-6,-6.7],[33,33], color=color, zorder=zorder, lw=lw)
    ax.plot([6,6.7],[30,30], color=color, zorder=zorder, lw=lw)
    ax.plot([-6,-6.7],[30,30], color=color, zorder=zorder, lw=lw)
    
    # For Shot Zones
    zone_1_text, zone_2_text, zone_3_text, zone_4_text, zone_5_text, zone_6_text, zone_7_text, zone_8_text, zone_9_text, zone_colors = calculateZones(df)
    
    ax.plot([-5.33,-13.65],[35.93,27.48], color='black', zorder=zorder, lw=lw)
    ax.plot([5.33,13.65],[35.93,27.48], color='black', zorder=zorder, lw=lw)
    ax.plot([-25, -18.9246],[36.1,36.1], color='black', zorder=zorder, lw=lw)
    ax.plot([25, 18.9246],[36.1,36.1], color='black', zorder=zorder, lw=lw)
    ax.plot([-8.2,-17.93],[23.8,0], color='black', zorder=zorder, lw=lw)
    ax.plot([8.2,17.93],[23.8,0], color='black', zorder=zorder, lw=lw)
    
    # Fill Shot Zones with Color
    y = np.arange(41.7375, 47, 0.1)
    y2 = np.arange(27.48, 41.75, 0.1)
    y3 = np.arange(35.93, 41.83, 0.1)
    y4 = np.arange(27.48, 35.93, 0.1)
    y5 = np.arange(22, 27.48, 0.1)
    y6 = np.arange(36.1, 41.75, 0.1)
    x = np.arange(-13.65, 13.65, 0.1)
    x2 = np.arange(-5.33, 5.33, 0.1)
    x3 = np.arange(-18.94, -8.2, 0.1)
    x4 = np.arange(8.2, 18.94, 0.1)
    x5 = np.arange(-8.2, 8.2, 0.1)
    m1, b1 = findLine(-19.75, 41.75, -13.65, 27.48)
    m2, b2 = findLine(19.75, 41.75, 13.65, 27.48)
    m3, b3 = findLine(-17.93, 0, -8.2, 23.8)
    m4, b4 = findLine(17.93, 0, 8.2, 23.8)
    
    text_box_fontsize = 15
    # Zone 1
    if zone_1_text != None:
        zone_1 = Circle((0, 41.75), radius=8, lw=lw, color=zone_colors[0], zorder=zorder, fill=True, alpha=0.5)
        ax.add_patch(zone_1)
        ax.text(0, 39, zone_1_text, fontsize=text_box_fontsize, bbox={'facecolor': zone_colors[0], 'alpha': 0.5, 'pad': 10}, ha='center', va='center')
    # Zone 2
    if zone_2_text != None:
        plt.fill_betweenx(y, x1 = -19.75, x2 = np.negative(np.sqrt(64 - (y - 41.75)**2)), color=zone_colors[1], alpha=0.5, linewidth=0.0)
        plt.fill_betweenx(y2, x1 = np.negative(np.sqrt(390.0625 - (y2 - 41.75)**2)), x2 = (y2 - b1) / m1, color=zone_colors[1], alpha=0.5, linewidth=0.0)
        plt.fill_betweenx(y3, x1 = (y3 - b1) / m1, x2 = np.negative(np.sqrt(64 - (y3 - 41.75)**2)), color=zone_colors[1], alpha=0.5, linewidth=0.0)
        plt.fill([-17.262, -13.65, -5.33], [35.93, 27.48, 35.93], color=zone_colors[1], alpha=0.5, linewidth=0.0)
        ax.text(-13, 39, zone_2_text, fontsize=text_box_fontsize, bbox={'facecolor': zone_colors[1], 'alpha': 0.5, 'pad': 10}, ha='center', va='center')
    # Zone 4
    if zone_4_text != None:
        plt.fill_betweenx(y, x1 = 19.75, x2 = np.sqrt(64 - (y - 41.75)**2), color=zone_colors[3], alpha=0.5, linewidth=0.0)
        plt.fill_betweenx(y2, x1 = np.sqrt(390.0625 - (y2 - 41.75)**2), x2 = (y2 - b2) / m2, color=zone_colors[3], alpha=0.5, linewidth=0.0)
        plt.fill_betweenx(y3, x1 = (y3 - b2) / m2, x2 = np.sqrt(64 - (y3 - 41.75)**2), color=zone_colors[3], alpha=0.5, linewidth=0.0)
        plt.fill([17.3, 13.75, 5.33], [35.93, 27.48, 35.93], color=zone_colors[3], alpha=0.5, linewidth=0.0)
        ax.text(13, 39, zone_4_text, fontsize=text_box_fontsize, bbox={'facecolor': zone_colors[3], 'alpha': 0.5, 'pad': 10}, ha='center', va='center')
    # Zone 3
    if zone_3_text != None:
        plt.fill_between(x, y1 = 41.75 - np.sqrt(390.0625 - x**2), y2 = 27.48, color=zone_colors[2], alpha=0.5, linewidth=0.0)
        plt.fill_between(x2, y1 = 41.75 - np.sqrt(64 - x2**2), y2 = 27.48, color=zone_colors[2], alpha=0.5, linewidth=0.0)
        plt.fill([-5.3, -5.3, -13.65], [35.93, 27.48, 27.48], color=zone_colors[2], alpha=0.5, linewidth=0.0)
        plt.fill([5.3, 5.3, 13.65], [35.93, 27.48, 27.48], color=zone_colors[2], alpha=0.5, linewidth=0.0)
        ax.text(0, 28, zone_3_text, fontsize=text_box_fontsize, bbox={'facecolor': zone_colors[2], 'alpha': 0.5, 'pad': 10}, ha='center', va='center')
    # Zone 5
    if zone_5_text != None:
        plt.fill([-25, -25, -19.75, -19.75], [47, 36.1, 36.1, 47], color=zone_colors[4], alpha=0.5, linewidth=0.0)
        plt.fill_betweenx(y6, x1 = -19.8, x2 = np.negative(np.sqrt(390.0625 - (y6 - 41.75)**2)), color=zone_colors[4], alpha=0.5, linewidth=0.0)
        ax.text(-22.5, 41, zone_5_text, fontsize=text_box_fontsize, bbox={'facecolor': zone_colors[4], 'alpha': 0.5, 'pad': 10}, ha='center', va='center')
    # Zone 9
    if zone_9_text != None:
        plt.fill([25, 25, 19.75, 19.75], [47, 36.1, 36.1, 47], color=zone_colors[8], alpha=0.5, linewidth=0.0)
        plt.fill_betweenx(y6, x1 = 19.7, x2 = np.sqrt(390.0625 - (y6 - 41.75)**2), color=zone_colors[8], alpha=0.5, linewidth=0.0)
        ax.text(22.5, 41, zone_9_text, fontsize=text_box_fontsize, bbox={'facecolor': zone_colors[8], 'alpha': 0.5, 'pad': 10}, ha='center', va='center')
    # Zone 6
    if zone_6_text != None:
        plt.fill([-25, -25, -18.925, -18.925], [36.1, 0, 0, 36.1], color=zone_colors[5], alpha=0.5, linewidth=0.0)
        plt.fill_between(x3, y1 = 41.75 - np.sqrt(390.0625 - x3**2), y2 = (m3 * x3) + b3, color=zone_colors[5], alpha=0.5, linewidth=0.0)
        ax.text(-19, 23, zone_6_text, fontsize=text_box_fontsize, bbox={'facecolor': zone_colors[5], 'alpha': 0.5, 'pad': 10}, ha='center', va='center')
    # Zone 8
    if zone_8_text != None:
        plt.fill([25, 25, 18.925, 18.925], [36.1, 0, 0, 36.1], color=zone_colors[7], alpha=0.5, linewidth=0.0)
        plt.fill_between(x4, y1 = 41.75 - np.sqrt(390.0625 - x4**2), y2 = (m4 * x4) + b4, color=zone_colors[7], alpha=0.5, linewidth=0.0)
        ax.text(19, 25, zone_8_text, fontsize=text_box_fontsize, bbox={'facecolor': zone_colors[7], 'alpha': 0.5, 'pad': 10}, ha='center', va='center')
    # Zone 7
    if zone_7_text != None:
        plt.fill([-8.2, -8.2, -17.93], [23.8, 0, 0], color=zone_colors[6], alpha=0.5, linewidth=0.0)
        plt.fill([8.1, 8.1, 17.93], [23.8, 0, 0], color=zone_colors[6], alpha=0.5, linewidth=0.0)
        plt.fill_between(x5, y1 = 41.75 - np.sqrt(390.0625 - x5**2), y2 = 0, color=zone_colors[6], alpha=0.5, linewidth=0.0)
        ax.text(0, 17, zone_7_text, fontsize=text_box_fontsize, bbox={'facecolor': zone_colors[6], 'alpha': 0.5, 'pad': 10}, ha='center', va='center')
    
    court_elements = [outer, center_circle, box, free_throw_fill, free_throw_dash, hoop, arc, top_rect, bottom_rect]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)
        

    plt.axis('off')
    plt.suptitle(f'{name} Heatmap', fontsize=25, color='white')
    plt.xlim([-26,26])
    plt.ylim([0,47])
    plt.tight_layout()
    plt.savefig(f'{file_path}{name}_heat_map.png', bbox_inches='tight')
    plt.close()
#     plt.show()
#     return fig, ax


        
    
    
if __name__ == '__main__':
    global fig, ax
    df = pd.read_csv('output/csv_files/as_vs_adsJul-11-2021.csv')
    draw_court_vertical(df)